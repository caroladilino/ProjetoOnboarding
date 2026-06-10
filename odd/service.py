import asyncio
import json
import random
from typing import Any

import nats
import redis.asyncio as redis
from nats.aio.msg import Msg

service_state: dict[str, Any] = {}


async def odd_number_request(msg: Msg) -> None:
    received_data = json.loads(msg.data.decode())
    requested_id = received_data.get("id")
    r = service_state["redis_client"]

    generated_number = random.randint(1, 100) * 2 + 1

    await r.set(f"number:{requested_id}", generated_number, ex=3600)
    answer = {"id": requested_id, "number": generated_number}
    print("odd number generated")
    await msg.respond(json.dumps(answer).encode())


async def main() -> None:
    r_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    service_state["redis_client"] = r_client
    print("[ODD] connected to redis")

    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("number.odd", cb=odd_number_request)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
