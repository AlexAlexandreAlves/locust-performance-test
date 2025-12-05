# Use a imagem oficial do Python como base
FROM python:3.14.1-alpine

# Defina o diretório de trabalho
WORKDIR /usr/src/app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o contêiner
COPY . .

# Comando para executar o Locust
CMD ["locust", "-f", "tests/activities_post_test.py", "--host", "http://localhost", "--headless", "-u", "10", "-r", "1", "--run-time", "15s", "--logfile", "locust.log"]