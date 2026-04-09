from fastapi import FastAPI
import uvicorn
from env.environment import SmartOpsEnv
from env.tasks import TASKS

app = FastAPI()

env = SmartOpsEnv(TASKS["easy"])

@app.get("/")
async def home():
    return {
        "message": "SmartOps OpenEnv is running",
        "usage": "POST /reset to start environment"
    }

@app.post("/reset")
async def reset():
    obs = await env.reset()
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