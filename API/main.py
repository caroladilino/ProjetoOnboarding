import json
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import nats
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException

# save the connection in a global dictionary so that all variables have access
app_state: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # only connects to the nats server once and saves the connection in the global dict
    nc = await nats.connect("nats://localhost:4222")
    app_state["nats_client"] = nc

    yield
    await nc.close()


app = FastAPI(title="Onboarding Project API", lifespan=lifespan)

# connects to REDIS
r = aioredis.Redis(host="localhost", port=6379, decode_responses=True)


@app.get("/")
def home() -> dict[str, str]:
    return {"status": "Server is online and working"}


@app.get("/history")
async def history() -> dict[str, int | dict[str, int]]:
    nc = app_state["nats_client"]

    nats_answer = await nc.request("history", json.dumps(None).encode(), timeout=2)

    data_response: dict[str, int | dict[str, int]] = json.loads(
        nats_answer.data.decode()
    )

    return data_response


@app.get("/even/{id}")
async def even(id: int) -> dict[str, int]:
    nc = app_state["nats_client"]

    payload = {"id": id}

    nats_answer = await nc.request(
        "number.even", json.dumps(payload).encode(), timeout=2
    )

    data_response: dict[str, int] = json.loads(nats_answer.data.decode())

    return data_response


@app.get("/odd/{id}")
async def odd(id: int) -> dict[str, int]:
    nc = app_state["nats_client"]

    payload = {"id": id}

    nats_answer = await nc.request(
        "number.odd", json.dumps(payload).encode(), timeout=2
    )

    data_response: dict[str, int] = json.loads(nats_answer.data.decode())

    return data_response


@app.get("/check/{id}")
async def check(id: int) -> int:
    nc = app_state["nats_client"]

    payload = {"id": id}

    nats_answer = await nc.request(
        "check.number", json.dumps(payload).encode(), timeout=2
    )

    data_response = json.loads(nats_answer.data.decode())

    answer = data_response.get("number")

    if answer is None:
        raise HTTPException(status_code=404, detail="id não testado")

    return int(answer)


@app.get("/save/{id}/{number}")
async def save(id: int, number: int) -> str:
    nc = app_state["nats_client"]

    payload = {"id": id, "number": number}

    await nc.request("save.number", json.dumps(payload).encode(), timeout=2)
    return "number was saved"
