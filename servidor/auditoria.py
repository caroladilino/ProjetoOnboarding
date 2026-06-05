import asyncio

import redis.asyncio as aioredis


async def auditoria_dos_pedidos() -> None:
    r = aioredis.Redis(host="localhost", port=6379, decode_responses=True)

    # pra printar todos pedidos "a parir de agora"
    ultimo_id_lido = "$"

    print("auditoria rodando!")

    while True:
        resultado = await r.xread(
            {"stream:auditoria": ultimo_id_lido}, count=1, block=0
        )

        for stream_nome, mensagens in resultado:
            for msg_id, dados in mensagens:
                print(f"\n [EVENTO DO STREAM DETECTADO - ID {msg_id}]")
                print(f"Ação: {dados.get('acao')}")
                print(f"ID da Requisição: {dados.get('id_requisicao')}")
                print(f"Valor Gerado: {dados.get('valor')}")

                ultimo_id_lido = msg_id

        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(auditoria_dos_pedidos())
