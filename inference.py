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
    prompt = f"Classify and respond:\nMessage: {obs.customer_message}\nReturn JSON with priority, department, response"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    try:
        data = json.loads(response.choices[0].message.content)
        return Action(**data)
    except:
        return Action(priority="medium", department="general", response="We are reviewing your issue.")

async def run_task(name):
    env = SmartOpsEnv(TASKS[name])
    obs = await env.reset()
    log_start(name, "smartops_env", MODEL_NAME)

    rewards = []
    for step in range(1,5):
        action = get_action(obs)
        result = await env.step(action)

        log_step(step, str(action), result["reward"], result["done"], None)

        rewards.append(result["reward"])
        if result["done"]:
            break
        obs = result["observation"]

    score = sum(rewards)/len(rewards)
    log_end(score>0.5, len(rewards), score, rewards)

async def main():
    for t in ["easy","medium","hard"]:
        await run_task(t)

if __name__=="__main__":
    asyncio.run(main())
