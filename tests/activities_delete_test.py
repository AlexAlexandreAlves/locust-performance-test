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

# Reads the configuration from the JSON file
with open(config_path, mode='r') as config_file:
    config = json.load(config_file)


class DetActivities(TaskSet):

    def on_start(self):
        self.activities = []
        with open(config_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.activities.append(row)

    @task
    def delete_activity(self):
        activity = random.choice(self.activities)

        response = self.client.delete("/api/v1/Activities/" + activity['id'])
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.text}")


class WebsiteUser(FastHttpUser):
    host = config['base_url']
    tasks = [DetActivities]
    wait_time = between(1, 5)


if __name__ == "__main__":
    run_single_user(DetActivities)
