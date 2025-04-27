#!/bin/sh

# executa as migraç`oes do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 --app-dir /fast_zero/src fast_zero.app:app