from fastapi import FastAPI
from env.environment import SmartOpsEnv
from env.tasks import TASKS

app = FastAPI()

env = SmartOpsEnv(TASKS["easy"])

@app.post("/reset")
async def reset():
    obs = await env.reset()
    return {"status": "ok", "observation": obs.dict()}
    
@app.get("/")
async def home():
    return {
        "message": "SmartOps OpenEnv is running",
        "usage": "POST /reset to start environment"
    }