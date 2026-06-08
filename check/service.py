import asyncio
import json
import random
from typing import Any

import nats
import redis.asyncio as redis
from nats.aio.msg import Msg

estado_servico: dict[str, Any] = {}

async def lidar_com_requisicao(msg: Msg) -> None:
    dados_recebidos = json.loads(msg.data.decode())
    id_requisicao = dados_recebidos.get("id")

    r = estado_servico["redis_cliente"]

    valor = await r.get(f"numero:{id_requisicao}")
    resposta = {"id": id_requisicao, "numero": valor}

    print("número checado")

    await msg.respond(json.dumps(resposta).encode())


async def main() -> None:
    r_cliente = redis.Redis(host="localhost", port=6379, decode_responses=True)
    estado_servico["redis_cliente"] = r_cliente
    print("[Serviço Números] Conectado ao Redis com sucesso!")

    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("requisicao.numero", cb=lidar_com_requisicao)


    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())