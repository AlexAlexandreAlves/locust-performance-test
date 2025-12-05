# Use a imagem oficial do Python como base
FROM python:3.14.1-alpine

# Instale as dependências do sistema necessárias para compilar pacotes
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev

# Defina o diretório de trabalho
WORKDIR /usr/src/app

# Copie o requirements.txt da raiz do projeto
COPY requirements.txt ./

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o contêiner
COPY . .

# Comando para executar o Locust
CMD ["locust", "-f", "locust-venv/tests/activities_post_test.py", "--headless", "-u", "10", "-r", "1", "--run-time", "15s"]
