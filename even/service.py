import asyncio
import json
import random
from typing import Any

import nats
import redis.asyncio as redis
from nats.aio.msg import Msg

service_state: dict[str, Any] = {}


async def even_number_request(msg: Msg) -> None:
    data_received = json.loads(msg.data.decode())
    requested_id = data_received.get("id")

    r = service_state["redis_client"]

    generated_number = random.randint(1, 100) * 2

    await r.set(f"number:{requested_id}", generated_number, ex=3600)

    # Sending message to REDIS Stream
    data_to_send = {
        "action": "generate_even_number",
        "id_of_request": str(requested_id),
        "value": str(generated_number),
    }

    await r.xadd("stream:logger", data_to_send, id="*")
    print("Message sent")

    answer = {"id": requested_id, "number": generated_number}
    print("even number generated")

    await msg.respond(json.dumps(answer).encode())


async def main() -> None:
    r_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    service_state["redis_client"] = r_client
    print("[EVEN] connected to redis")

    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("number.even", cb=even_number_request)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
