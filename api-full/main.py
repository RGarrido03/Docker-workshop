# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncpg
import os

app = FastAPI()

# Database connection details (replace with your own)
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_URL = os.environ.get("POSTGRES_URL", "db")
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}"
)


class Item(BaseModel):
    name: str
    description: str = None


async def get_connection():
    return await asyncpg.connect(DATABASE_URL)


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()


async def init_db():
    conn = await get_connection()
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT
        )
    """
    )
    await conn.close()


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    async with app.state.pool.acquire() as conn:
        record = await conn.fetchrow(
            "INSERT INTO items(name, description) VALUES($1, $2) RETURNING id, name, description",
            item.name,
            item.description,
        )
    return dict(record)


@app.get("/items/", response_model=List[Item])
async def read_items():
    async with app.state.pool.acquire() as conn:
        records = await conn.fetch("SELECT id, name, description FROM items")
    return [dict(record) for record in records]


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    async with app.state.pool.acquire() as conn:
        record = await conn.fetchrow(
            "SELECT id, name, description FROM items WHERE id = $1", item_id
        )
    if not record:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(record)


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    async with app.state.pool.acquire() as conn:
        result = await conn.execute("DELETE FROM items WHERE id = $1", item_id)
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}


# Initialize database on startup
@app.on_event("startup")
async def on_startup():
    await init_db()
