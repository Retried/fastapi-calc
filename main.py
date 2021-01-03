import uvicorn
import math
from fastapi import FastAPI
from enum import Enum


class select(Enum):
    sum = "sum"
    subtraction = "subtraction"
    multiplication = "multiplication"
    division = "division"
    exponentiation = "exponentiation"
    root = "root"


app = FastAPI()


@app.get("/calc")
def read_item(mode: select, x: int, y: int):
    if mode == mode.sum:
        return x + y

    if mode == mode.subtraction:
        return x - y

    if mode == mode.multiplication:
        return x * y

    if mode == mode.division:
        if y == 0:
            return "Error: Dividing by 0"
        else:
            return x / y

    if mode == mode.exponentiation:
        return math.pow(x, y)

    if mode == mode.root:
        return math.pow(x, 1 / y)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
