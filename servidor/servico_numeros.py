import asyncio
import json
import random
import redis.asyncio as redis
import nats
from nats.aio.msg import Msg

estado_servico = {}

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


async def main() -> None:
    r_cliente = redis.Redis(host="localhost", port=6379, decode_responses=True)
    estado_servico["redis_cliente"] = r_cliente
    print("[Serviço Números] Conectado ao Redis com sucesso!")
    
    nc = await nats.connect("nats://localhost:4222")

    await nc.subscribe("numeros.par", cb=lidar_com_pedido_par)
    await nc.subscribe("numeros.impar", cb=lidar_com_pedido_impar)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
