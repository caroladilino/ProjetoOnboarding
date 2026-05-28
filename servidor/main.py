from fastapi import FastAPI, HTTPException
import redis

app = FastAPI(title="API de Teste Técnico")

# Conecta ao Redis (ajuste o host se necessário)
# Em ambiente de teste, localhost costuma ser o padrão
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.get("/")
def home():
    return {"status": "Servidor online e operante!"}

@app.post("/salvar")
def salvar_chave(key: str, value: str):
    try:
        # Salva no Redis com um tempo de expiração (TTL) de 10 minutos
        r.set(key, value, ex=600)
        return {"mensagem": f"Chave '{key}' salva com sucesso!"}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Não foi possível conectar ao Redis")

@app.get("/buscar/{key}")
def buscar_chave(key: str):
    try:
        value = r.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Chave não encontrada ou expirada")
        return {"chave": key, "valor": value}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Não foi possível conectar ao Redis")
