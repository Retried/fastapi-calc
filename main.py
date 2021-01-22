import uvicorn
from fastapi import FastAPI, Response, status
from enum import Enum


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
    version="2.0.1"
)


@app.get("/calc", status_code=status.HTTP_201_CREATED)
def read_item(mode: Select, response: Response, x: int, y: int = 0):
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
        return cases[mode.value](x, y)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", debug=True)
