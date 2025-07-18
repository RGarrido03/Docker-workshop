from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("{name}")
async def hello_name(name: str):
    return {"message": f"Hello {name}"}
