import random

import redis
from fastapi import FastAPI, HTTPException

app = FastAPI(title="API de Teste Técnico")

# Conecta ao Redis (ajuste o host se necessário)
# Em ambiente de teste, localhost costuma ser o padrão
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

historico: dict[int, int] = {}


@app.get("/")
def home() -> dict[str, str]:
    return {"status": "Servidor online e operante!"}


@app.get("/validacao")
def texto() -> dict[int, int]:
    return historico


@app.get("/numeropar/{id}")
def numero_par(id: int) -> int:
    c = random.randint(1, 100) * 2
    historico[id] = c
    return c


@app.get("/numeroimpar/{id}")
def numero_impar(id: int) -> int:
    c = random.randint(1, 100)
    if c % 2 != 0:
        historico[id] = c
        return c
    else:
        historico[id] = c + 1
        return c + 1


@app.get("/requisicao/{id}")
def requisicao(id: int) -> int:
    valor = historico.get(id)

    if valor is None:
        raise HTTPException(status_code=404, detail="id não testado")

    return valor


@app.get("/salvar/{id}/{numero}")
def salvar(id: int, numero: int) -> str:
    historico[id] = numero
    return "numero salvo com sucesso"


@app.post("/salvar")
def salvar_chave(key: str, value: str) -> dict[str, str]:
    try:
        # Salva no Redis com um tempo de expiração (TTL) de 10 minutos
        r.set(key, value, ex=600)
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
