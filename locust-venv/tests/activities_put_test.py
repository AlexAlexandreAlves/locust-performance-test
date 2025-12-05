from locust import FastHttpUser, TaskSet, task, between, run_single_user
import os
import json
import csv
import random
import logging


# Define o caminho absoluto para o arquivo de configuração
config_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../config.json')

# Define o caminho absoluto para o arquivo csv que busca atividades por ID
config_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/get_activities_by_id.csv')

# Define o caminho absoluto para o arquivo que contém os dados para atualizar as atividades
config_update_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/put_activities.csv')

# Define o caminho absoluto para o arquivo json de atividades
config_data_json = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/json/activities.json')


# Lê a configuração do arquivo JSON
with open(config_path, mode='r') as config_file:
    config = json.load(config_file)


class PutActivities(TaskSet):

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

        # Lê o arquivo CSV de atualização e armazena os dados em uma lista
        self.update_data = []
        with open(config_update_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.update_data.append(row)

    @task
    def put_activity(self):
        # Seleciona uma atividade aleatória da lista
        activity = random.choice(self.activities)
        # Seleciona um título aleatório da lista de atualização
        update_info = random.choice(self.update_data)
        # Cria um payload a partir do payload base
        payload = self.base_payload.copy()
        # Substitui o título pelo valor do CSV de atualização
        payload['title'] = update_info['title']
        # Envia o request PUT
        response = self.client.put("/api/v1/Activities/" + activity['id'], json=payload)
        # Registra o status code e o conteúdo da resposta no log
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.text}")


class WebsiteUser(FastHttpUser):
    # Define a URL base para os testes a partir da configuração
    host = config['base_url']
    tasks = [PutActivities]
    wait_time = between(1, 5)


if __name__ == "__main__":
    run_single_user(PutActivities)