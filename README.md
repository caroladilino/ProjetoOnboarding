colinha para rodar em outra máquina linux:

1. comando para criar o ambiente virtual 
    python3 -m venv .venv

2. abra o ambiente virtual
    source .venv/bin/activate

3. instalar as dependências
    pip install -r requirements.txt

4. rodar o servidor
    cd servidor
    uvicorn main:app --reload

5. rodar o cliente (abra outro terminal)
    python client.py