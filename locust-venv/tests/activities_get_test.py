from locust import FastHttpUser, TaskSet, task, between, run_single_user
import os
import json
import csv
import random
import logging


# Define o caminho absoluto para o arquivo de configuração
config_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../config.json')

# Define o caminho absoluto para o arquivo csv de dados
config_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/get_activities_by_id.csv')

# Lê a configuração do arquivo JSON
with open(config_path, mode='r') as config_file:
    config = json.load(config_file)


class GetActivities(TaskSet):

    def on_start(self):
        # Lê o arquivo CSV e armazena os dados em uma lista
        self.activities = []
        with open(config_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.activities.append(row)

    @task
    def get_people(self):
        self.client.get("/api/v1/Activities")

    @task
    def get_starships(self):
        activity = random.choice(self.activities)

        response = self.client.get("/api/v1/Activities/" + activity['id'])
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.text}")


class WebsiteUser(FastHttpUser):
    # Define a URL base para os testes a partir da configuração
    host = config['base_url']
    tasks = [GetActivities]
    wait_time = between(1, 5)


if __name__ == "__main__":
    run_single_user(GetActivities)
