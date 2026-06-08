# cheatsheet to run the code


### Terminal 1

start nats server

    nats-server

### Terminal 2

turn on the api

    cd API
    source ../.venv/bin/activate
    uvicorn main:app --reload

### Terminal 3..n 

run each service in a dedicated terminal

    cd desired_folder
    uv run service.py

<br>
<br>

# before commiting:

    ruff format
    ruff check --fix
    mypy .
