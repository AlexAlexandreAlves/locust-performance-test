from locust import FastHttpUser, TaskSet, task, between, run_single_user
import os
import json
import csv
import random
import logging


config_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../config.json')

config_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/get_activities_by_id.csv')

config_update_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/put_activities.csv')

config_data_json = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/json/activities.json')


with open(config_path, mode='r') as config_file:
    config = json.load(config_file)


class PutActivities(TaskSet):

    def on_start(self):
        self.activities = []
        with open(config_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.activities.append(row)

        with open(config_data_json, mode='r') as file:
            self.base_payload = json.load(file)

        # Reads the update CSV file and stores the data in a list
        self.update_data = []
        with open(config_update_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.update_data.append(row)

    @task
    def put_activity(self):
        activity = random.choice(self.activities)
        # Select a random title from the update list
        update_info = random.choice(self.update_data)
        payload = self.base_payload.copy()
        # Chnage the title in the payload to the one from the update CSV
        payload['title'] = update_info['title']
        response = self.client.put("/api/v1/Activities/" + activity['id'], json=payload)
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.text}")


class WebsiteUser(FastHttpUser):
    host = config['base_url']
    tasks = [PutActivities]
    wait_time = between(1, 5)


if __name__ == "__main__":
    run_single_user(PutActivities)