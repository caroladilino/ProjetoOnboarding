import asyncio
import json
import random
from typing import Any

import nats
import redis.asyncio as redis
from nats.aio.msg import Msg

estado_servico: dict[str, Any] = {}

async def lidar_com_salvar(msg: Msg) -> None:
    dados_recebidos = json.loads(msg.data.decode())
    id_requisicao = dados_recebidos.get("id")
    numero_requisicao = dados_recebidos.get("numero")

    r = estado_servico["redis_cliente"]

    await r.set(f"numero:{id_requisicao}", numero_requisicao, ex=3600)
    print("número salvo")

    await msg.respond(b"OK")

async def main() -> None:
    r_cliente = redis.Redis(host="localhost", port=6379, decode_responses=True)
    estado_servico["redis_cliente"] = r_cliente
    print("[Serviço Números] Conectado ao Redis com sucesso!")

    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("salvar.numero", cb=lidar_com_salvar)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())