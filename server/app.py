from fastapi import FastAPI
import uvicorn
from env.environment import SmartOpsEnv
from env.tasks import TASKS

app = FastAPI()

env = None  # lazy init


def get_env():
    global env
    if env is None:
        env = SmartOpsEnv(TASKS["easy"])
    return env


@app.get("/")
async def home():
    return {
        "message": "SmartOps OpenEnv running",
        "usage": "POST /reset"
    }


@app.post("/reset")
async def reset():
    env_instance = get_env()
    obs = await env_instance.reset()
    return {"status": "ok", "observation": obs.dict()}


def main():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=False
    )


if __name__ == "__main__":
    main()