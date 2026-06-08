import asyncio
import json
import random
from typing import Any

import nats
import redis.asyncio as redis
from nats.aio.msg import Msg

service_state: dict[str, Any] = {}

async def check_number(msg: Msg) -> None:
    data_received = json.loads(msg.data.decode())
    requested_id = data_received.get("id")

    r = service_state["redis_client"]

    value = await r.get(f"number:{requested_id}")
    answer = {"id": requested_id, "number": value}

    print("number was checked")

    await msg.respond(json.dumps(answer).encode())


async def main() -> None:
    r_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    service_state["redis_client"] = r_client
    print("[CHECK] connected to redis")

    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("check.number", cb=check_number)


    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())