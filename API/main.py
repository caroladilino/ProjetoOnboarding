import json
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import nats
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException

# guardar a conexão do nats em um dicionário global para que todas as rotas enham acesso
estado_app: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # quando liga a api vai se conectar ao nats (uma vez só)
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
    nc = estado_app["nats_cliente"]

    resposta_nats = await nc.request("validar", json.dumps(None).encode(), timeout=2)

    dados_resposta: dict[str, int | dict[str, int]] = json.loads(
        resposta_nats.data.decode()
    )

    return dados_resposta


@app.get("/numeropar/{id}")
async def numero_par(id: int) -> dict[str, int]:
    # pega a conexão do NATS que guardamos no dicionário lá em cima
    nc = estado_app["nats_cliente"]

    # prepara os dados que vamos enviar no msg
    payload = {"id": id}

    # envia o msg e espera a resposta
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
        "requisicao.numero", json.dumps(payload).encode(), timeout=2
    )

    dados_recebidos = json.loads(resposta_nats.data.decode())

    valor = dados_recebidos.get("numero")

    if valor is None:
        raise HTTPException(status_code=404, detail="id não testado")

    return int(valor)


@app.get("/salvar/{id}/{numero}")
async def salvar(id: int, numero: int) -> str:
    nc = estado_app["nats_cliente"]

    payload = {"id": id, "numero": numero}

    await nc.request("salvar.numero", json.dumps(payload).encode(), timeout=2)
    return "numero salvo com sucesso"
