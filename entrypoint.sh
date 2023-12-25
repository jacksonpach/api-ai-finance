#!/bin/bash

# Iniciar o serviço SSHD em background
/usr/sbin/sshd

# Executar o Uvicorn para iniciar a aplicação FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

exec "$@"
