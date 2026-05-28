import time
from typing import Any

import requests

BASE_URL: str = "http://127.0.0.1:8000"


def executar_fluxo_teste() -> None:
    print("🚀 Iniciando testes do cliente...\n")

    # 1. Testar se o servidor está vivo
    print("1. Testando conexão com o servidor...")
    res: requests.Response = requests.get(f"{BASE_URL}/")
    dados_1: Any = res.json()
    print(f"Resposta: {dados_1}\n")

    # 2. Enviar um dado para salvar no Redis através da API
    print("2. Enviando dados para salvar ('tecnologia': 'FastAPI+Redis')...")
    payload: dict[str, str] = {"key": "tecnologia", "value": "FastAPI+Redis"}
    res = requests.post(f"{BASE_URL}/salvar", params=payload)
    dados_2: Any = res.json()
    print(f"Resposta: {dados_2}\n")

    # 3. Buscar o dado que acabamos de salvar
    print("3. Buscando a chave 'tecnologia'...")
    res = requests.get(f"{BASE_URL}/buscar/tecnologia")
    dados_3: Any = res.json()
    print(f"Resposta: {dados_3}\n")

    # 4. Testar busca de algo que não existe
    print("4. Testando busca de chave inexistente...")
    res = requests.get(f"{BASE_URL}/buscar/chave_fantasma")
    dados_4: Any = res.json()
    print(f"Resposta (Status {res.status_code}): {dados_4}\n")


if __name__ == "__main__":
    # Dá um pequeno delay caso queira rodar scripts em sequência
    time.sleep(1)
    executar_fluxo_teste()
