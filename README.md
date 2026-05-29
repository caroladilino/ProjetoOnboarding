colinha para rodar em outra máquina linux:

1. comando para criar o ambiente virtual 
    uv venv

2. abra o ambiente virtual
    source .venv/bin/activate

3. instalar os pacotes que vamos usar
    uv pip install -r requirements.txt

4. rodar o servidor
    cd servidor
    uvicorn main:app --reload

5. rodar o cliente (abra outro terminal)
    python client.py


antes de dar o commit rodar comandos:

ruff format

ruff check --fix

mypy .
