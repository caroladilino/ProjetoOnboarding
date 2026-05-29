import random

import redis
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException

app = FastAPI(title="API de Teste Técnico")

# Conecta ao Redis (ajuste o host se necessário)
# Em ambiente de teste, localhost costuma ser o padrão
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
async def numero_par(id: int) -> int:
    c = random.randint(1, 100) * 2

    await r.set(f"numero:{id}", c, ex=3600)

    # historico[id] = c
    return c


@app.get("/numeroimpar/{id}")
async def numero_impar(id: int) -> int:
    c = random.randint(1, 100) * 2 + 1
    await r.set(f"numero:{id}", c, ex=3600)
    return c


@app.get("/requisicao/{id}")
async def requisicao(id: int) -> int:

    valor = await r.get(f"numero:{id}")

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
