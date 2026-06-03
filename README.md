colinha para rodar

Terminal 0
    sudo systemctl start redis-server
    -- ligar o REDIS

Terminal 1
    nats-server
    -- servidor nats

Terminal 2
    cd servidor
    source ../.venv/bin/activate
    python servico_numeros.py
    -- na pasta servidor ligar o ambiente virtual e rodar o arquivo dos serviços

Terminal 3
    cd servidor
    source ../.venv/bin/activate
    uvicorn main:app --reload
    -- na pasta servidor, ligar o ambiente virtual e rodar o main


antes de dar o commit rodar comandos:

ruff format

ruff check --fix

mypy .
