import asyncio
import json
import random
from typing import Any

import nats
import redis.asyncio as redis
from nats.aio.msg import Msg

service_state: dict[str, Any] = {}

async def save_number(msg: Msg) -> None:
    received_data = json.loads(msg.data.decode())
    requested_id = received_data.get("id")
    requested_number = received_data.get("number")

    r = service_state["redis_client"]

    await r.set(f"number:{requested_id}", requested_number, ex=3600)
    print("number was saved")

    await msg.respond(b"OK")

async def main() -> None:
    r_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    service_state["redis_client"] = r_client
    print("[SAVE] connected to redis")

    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("save.number", cb=save_number)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())