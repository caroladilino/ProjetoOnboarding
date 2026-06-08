# Cheatsheet to run the code


### Terminal 1

Start nats server

    nats-server

### Terminal 2

Turn on the api

    cd API
    source ../.venv/bin/activate
    uvicorn main:app --reload

### Terminal 3..n 

Run each service in a dedicated terminal

    cd desired_folder
    uv run service.py

<br>
<br>

# Before commiting:

    ruff format
    ruff check --fix
    mypy .
