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

    for chave in chaves:
        valor = await r.get(chave)
        if valor is not None:
            dados_internos[chave] = int(valor)

    resposta = {
        "total_chaves": len(chaves), 
        "dados": dados_internos
    }

    print("Validação do cache processada e enviada!")

    await msg.respond(json.dumps(resposta).encode())


async def lidar_com_pedido_par(msg: Msg) -> None:
    dados_recebidos = json.loads(msg.data.decode())
    id_requisicao = dados_recebidos.get("id")

    r = estado_servico["redis_cliente"]

    numero_gerado = random.randint(1, 100) * 2

    await r.set(f"numero:{id_requisicao}", numero_gerado, ex=3600)

    resposta = {"id": id_requisicao, "numero": numero_gerado}
    print("numero par gerado! uhul")

    await msg.respond(json.dumps(resposta).encode())


async def lidar_com_pedido_impar(msg: Msg) -> None:
    dados_recebidos = json.loads(msg.data.decode())
    id_requisicao = dados_recebidos.get("id")
    r = estado_servico["redis_cliente"]

    numero_gerado = random.randint(1, 100) * 2 + 1

    await r.set(f"numero:{id_requisicao}", numero_gerado, ex=3600)
    resposta = {"id": id_requisicao, "numero": numero_gerado}
    print("numero impar gerado! uhul")
    await msg.respond(json.dumps(resposta).encode())


async def lidar_com_requisicao(msg: Msg) -> None:
    dados_recebidos = json.loads(msg.data.decode())
    id_requisicao = dados_recebidos.get("id")

    r = estado_servico["redis_cliente"]

    valor = await r.get(f"numero:{id_requisicao}")
    resposta = {"id": id_requisicao, "numero": valor}

    print("número checado")

    await msg.respond(json.dumps(resposta).encode())

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

    await nc.subscribe("validar", cb=lidar_com_validacao)
    await nc.subscribe("numeros.par", cb=lidar_com_pedido_par)
    await nc.subscribe("numeros.impar", cb=lidar_com_pedido_impar)
    await nc.subscribe("requisicao.numero", cb=lidar_com_requisicao)
    await nc.subscribe("salvar.numero", cb=lidar_com_salvar)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
