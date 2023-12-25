# Utilizar a imagem base do Python
FROM python:3.11-slim-buster

# Definir variáveis de ambiente para Python
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH='/app'

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update -y \
    && apt-get install -y netcat gcc curl openssh-server \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false

# Copiar o arquivo pyproject.toml e o código da aplicação para o contêiner
COPY ./pyproject.toml .
COPY ./app ./app
COPY ./main.py .

# Instalar dependências do projeto
RUN poetry install

# Preparar o ambiente para depuração remota e SSHD
RUN python -m pip install --upgrade pip \
    && pip install pydevd-pycharm~=232.9559.58 \
    && pip install trio~=0.22.2 \
    && mkdir /var/run/sshd \
    && useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test \
    && echo 'test:test' | chpasswd \
    && sed -i 's/#PasswordAuthentication prohibit-password/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Copiar e tornar o script entrypoint executável
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expor as portas para Uvicorn e SSHD
EXPOSE 22
EXPOSE 8000

# Definir o script entrypoint como ponto de entrada
ENTRYPOINT ["/entrypoint.sh"]
