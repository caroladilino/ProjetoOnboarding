import json
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import nats
import redis
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException

# guardar a conexão do nats em um dicionário global para que todas as rotas enham acesso
estado_app: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Executa ao ligar a API: Conecta ao NATS uma única vez
    nc = await nats.connect("nats://localhost:4222")
    estado_app["nats_cliente"] = nc

    yield

    await nc.close()


app = FastAPI(title="API de Teste Técnico", lifespan=lifespan)

# Conecta ao Redis
r = aioredis.Redis(host="localhost", port=6379, decode_responses=True)


@app.get("/")
def home() -> dict[str, str]:
    return {"status": "Servidor online e operante!"}


@app.get("/validacao")
async def texto() -> dict[str, int | dict[str, int]]:
    chaves = await r.keys("numero:*")
    dados_internos = {}

    for chave in chaves:
        valor = await r.get(chave)
        if valor is not None:
            dados_internos[chave] = int(valor)

    return {"total_chaves": len(chaves), "dados": dados_internos}


@app.get("/numeropar/{id}")
async def numero_par(id: int) -> dict[str, int]:
    # pega a conexão do NATS que guardamos no dicionário lá em cima
    nc = estado_app["nats_cliente"]

    # prepara os dados que vamos enviar no msg
    payload = {"id": id}

    # Envia o pedido para o tópico "numeros.par" e ESPERA (request) a resposta.
    resposta_nats = await nc.request(
        "numeros.par", json.dumps(payload).encode(), timeout=2
    )

    # transforma a resposta em um dicionário e retorna
    dados_resposta: dict[str, int] = json.loads(resposta_nats.data.decode())

    return dados_resposta


@app.get("/numeroimpar/{id}")
async def numero_impar(id: int) -> dict[str, int]:
    nc = estado_app["nats_cliente"]

    payload = {"id": id}

    resposta_nats = await nc.request(
        "numeros.impar", json.dumps(payload).encode(), timeout=2
    )

    dados_resposta: dict[str, int] = json.loads(resposta_nats.data.decode())

    return dados_resposta


@app.get("/requisicao/{id}")
async def requisicao(id: int) -> int:
    nc = estado_app["nats_cliente"]

    payload = {"id": id}

    resposta_nats = await nc.request(
        "requisicao", json.dumps(payload).encode(), timeout=2
    )

    dados_recebidos = json.loads(resposta_nats.data.decode())

    valor = dados_recebidos.get("numero")

    if valor is None:
        raise HTTPException(status_code=404, detail="id não testado")

    return int(valor)


@app.get("/salvar/{id}/{numero}")
async def salvar(id: int, numero: int) -> str:
    await r.set(f"numero:{id}", numero, ex=3600)
    return "numero salvo com sucesso"


# funções que interagem com o arquivo cliente, ajeitar depois
@app.post("/salvar")
async def salvar_chave(key: str, value: str) -> dict[str, str]:  # 1. Adicionado 'async'
    try:
        # 2. Adicionado 'await' aqui
        await r.set(key, value, ex=600)
        return {"mensagem": f"Chave '{key}' salva com sucesso!"}
    except redis.ConnectionError:
        raise HTTPException(
            status_code=500, detail="Não foi possível conectar ao Redis"
        )


@app.get("/buscar/{key}")
def buscar_chave(key: str) -> dict[str, str]:
    try:
        value = r.get(key)
        if value is None:
            raise HTTPException(
                status_code=404, detail="Chave não encontrada ou expirada"
            )

        valor_str: str = str(value)

        return {"chave": key, "valor": valor_str}
    except redis.ConnectionError:
        raise HTTPException(
            status_code=500, detail="Não foi possível conectar ao Redis"
        )
