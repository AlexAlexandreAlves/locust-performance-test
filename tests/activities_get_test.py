from locust import FastHttpUser, TaskSet, task, between, run_single_user
import os
import json
import csv
import random
import logging


# Define the asbolute path to the configuration file
config_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../config.json')

# Define the absolute path to the csv file that fetches activities by ID
config_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/get_activities_by_id.csv')

# Reads the configuration from the JSON file
with open(config_path, mode='r') as config_file:
    config = json.load(config_file)


class GetActivities(TaskSet):

    def on_start(self):
        # Reads the CSV file and stores the data in a list
        self.activities = []
        with open(config_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.activities.append(row)

    @task
    def get_activity(self):
        self.client.get("/api/v1/Activities")

    @task
    def get_activity_by_id(self):
        activity = random.choice(self.activities)

        response = self.client.get("/api/v1/Activities/" + activity['id'])
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.text}")


class WebsiteUser(FastHttpUser):
    # Define the base URL from the configuration
    host = config['base_url']
    tasks = [GetActivities]
    wait_time = between(1, 5)


if __name__ == "__main__":
    run_single_user(GetActivities)
