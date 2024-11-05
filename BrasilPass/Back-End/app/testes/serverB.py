import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import httpx
import uvicorn

async def check_heartbeat():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get("http://localhost:8001/heartbeat/")
                if response.status_code == 200:
                    print("Service A is alive")
                else:
                    print("Service A is down")
            except Exception as e:
                print("Service A caiu:", e)

            await asyncio.sleep(5) 

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(check_heartbeat())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

@app.get("/heartbeat/")
async def heartbeat():
    return {"status": "alive"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
