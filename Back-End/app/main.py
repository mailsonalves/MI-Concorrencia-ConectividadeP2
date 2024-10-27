from fastapi import FastAPI
from routers.router import api_router
import uvicorn
from asyncio import run

app = FastAPI(title="Passcom_api")
app.include_router(api_router)


@app.get("/", summary="home", tags=["home"])
def teste() -> str:
    return "teste"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
