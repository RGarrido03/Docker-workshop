import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

myenv = os.environ.get("MYENV", None)


@app.get("/")
async def root():
    return {"message": "Hello World from the hot reload example"}


@app.get("{name}")
async def hello_name(name: str):
    return {"message": f"Hello {name}"}


@app.get("/env")
async def env_path():
    return {"message": "Environment variable MYENV is set to", "value": myenv}
