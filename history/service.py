import asyncio
import json
import random
from typing import Any

import nats
import redis.asyncio as redis
from nats.aio.msg import Msg

estado_servico: dict[str, Any] = {}


async def lidar_com_validacao(msg: Msg) -> None:
    r = estado_servico["redis_cliente"]

    chaves = await r.keys("numero:*")
    dados_internos = {}

    if chaves:
        valores = await r.mget(chaves)

        for chave, valor in zip(chaves, valores):
            if valor is not None:
                dados_internos[chave] = int(valor)

    resposta = {"total_chaves": len(chaves), "dados": dados_internos}
    print("Validação do cache processada e enviada!")
    await msg.respond(json.dumps(resposta).encode())



async def main() -> None:
    r_cliente = redis.Redis(host="localhost", port=6379, decode_responses=True)
    estado_servico["redis_cliente"] = r_cliente
    print("[Serviço Números] Conectado ao Redis com sucesso!")

    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("validar", cb=lidar_com_validacao)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
