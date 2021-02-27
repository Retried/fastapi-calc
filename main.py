from enum import Enum
from typing import List

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel


DATABASE_URL = "postgresql://postgres:8848@host.docker.internal:5432/database"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
history = sqlalchemy.Table(
    "history",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("data", sqlalchemy.Float, nullable=False)
)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


class Select(Enum):
    sum = "sum"
    subtraction = "subtraction"
    multiplication = "multiplication"
    division = "division"
    exponentiation = "exponentiation"
    root = "root"


app = FastAPI(
    title="FastAPI Calculator",
    description="My first project with FastAPI",
    version="3.0.0"
)


class Note(BaseModel):
    id: int
    data: float = 0


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/calc/", status_code=status.HTTP_201_CREATED)
async def calculate(mode: Select, response: Response, x: int, y: int = 0):
    cases = {
        "sum": lambda a, b: a + b,
        "subtraction": lambda a, b: a - b,
        "multiplication": lambda a, b: a * b,
        "division": lambda a, b: a / b,
        "exponentiation": lambda a, b: pow(a, b),
        "root": lambda a, b: pow(a, 1 / b),
    }

    if mode.value == "division" and y == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Error: Dividing by 0"
    elif mode.value == "root" and y == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Error: Root of 0"
    else:
        query = history.insert().values(data=cases[mode.value](x, y))
        await database.execute(query)
        return cases[mode.value](x, y)


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = history.select()
    return await database.fetch_all(query)


@app.get("/clear/")
async def delete_notes():
    query = history.delete()
    await database.execute(query)
    return 'Database is clear'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info", debug=True)
