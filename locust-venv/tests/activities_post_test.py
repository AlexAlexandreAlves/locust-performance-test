import csv
import json
import os
import logging
from locust import FastHttpUser, TaskSet, task, between, run_single_user
import random

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# Define o caminho absoluto para o arquivo de configuração
config_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../config.json')
# Define o caminho absoluto para o arquivo csv de dados
config_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/post_activities.csv')
# Define o caminho absoluto para o arquivo json de atividades
config_data_json = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/json/activities.json')

# Lê a configuração do arquivo JSON
with open(config_path, mode='r') as config_file:
    config = json.load(config_file)


class PostActivities(TaskSet):
    def on_start(self):
        # Lê o arquivo CSV e armazena os dados em uma lista
        self.activities = []
        with open(config_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.activities.append(row)

        # Lê o payload base do arquivo JSON
        with open(config_data_json, mode='r') as file:
            self.base_payload = json.load(file)

    @task
    def post_activities(self):
        # Seleciona uma atividade aleatória da lista
        if self.activities:  # Verifica se ainda há atividades disponíveis
            # Escolhe uma atividade aleatória
            activity = random.choice(self.activities)

            # Cria um payload a partir do payload base
            payload = self.base_payload.copy()  # Faz uma cópia do payload base
            # Substitui o título pelo valor do CSV
            payload['title'] = activity['title']
            # Substitui o valor de completed
            payload['completed'] = activity['completed'] == 'True'

            response = self.client.post(
                "/api/v1/Activities", json=payload
            )
            # Registra o status code e o conteúdo da resposta no log
            logging.info(f"Status Code: {response.status_code}")
            logging.info(f"Response Body: {response.text}")


class WebsiteUser(FastHttpUser):
    # Define a URL base para os testes a partir da configuração
    host = config['base_url']
    tasks = [PostActivities]
    wait_time = between(1, 5)


if __name__ == "__main__":
    run_single_user(PostActivities)
