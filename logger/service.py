import asyncio

import redis.asyncio as aioredis


async def request_logger() -> None:
    r = aioredis.Redis(host="localhost", port=6379, decode_responses=True)

    # Print only the requests starting now
    last_id = "$"

    print("Logger working")

    while True:
        result = await r.xread(
            {"stream:logger": last_id}, count=1, block=0
        )

        for this_stream, messages in result:
            for msg_id, data in messages:
                print(f"\n [DETECTED EVENT - {msg_id}]")
                print(f"Request: {data.get('action')}")
                print(f"ID: {data.get('id_of_request')}")
                print(f"Generated value: {data.get('value')}")

                last_id = msg_id

        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(request_logger())
