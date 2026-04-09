import os, asyncio, json
from openai import OpenAI
from env.environment import SmartOpsEnv
from env.tasks import TASKS
from env.models import Action

API_KEY = os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

def get_action(obs):
    try:
        prompt = f"Classify and respond:\nMessage: {obs.customer_message}"

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        try:
            data = json.loads(content)
            return Action(**data)
        except Exception:
            return Action(
                priority="medium",
                department="general",
                response=content[:100]
            )

    except Exception as e:
        print(f"[DEBUG] LLM failed: {e}", flush=True)
        return Action(
            priority="medium",
            department="general",
            response="We are reviewing your issue."
        )

async def run_task(name):
    env = SmartOpsEnv(TASKS[name])
    rewards = []
    steps = 0
    score = 0.0
    success = False

    log_start(name, "smartops_env", MODEL_NAME)

    try:
        obs = await env.reset()

        for step in range(1, 6):
            try:
                action = get_action(obs)

                result = await env.step(action)

                reward = result.get("reward", 0.0)
                done = result.get("done", False)

                log_step(step, str(action), reward, done, None)

                rewards.append(reward)
                steps = step

                if done:
                    break

                obs = result.get("observation")

            except Exception as step_error:
                print(f"[DEBUG] Step error: {step_error}", flush=True)
                log_step(step, "error", 0.0, True, str(step_error))
                break

        if rewards:
            score = sum(rewards) / len(rewards)
        else:
            score = 0.0

        success = score > 0.5

    except Exception as e:
        print(f"[DEBUG] Task failed: {e}", flush=True)

    finally:
        log_end(success, steps, score, rewards)

async def main():
    for t in ["easy", "medium", "hard"]:
        try:
            await run_task(t)
        except Exception as e:
            print(f"[DEBUG] Fatal error in task {t}: {e}", flush=True)
            log_end(False, 0, 0.0, [])

if __name__=="__main__":
    asyncio.run(main())
