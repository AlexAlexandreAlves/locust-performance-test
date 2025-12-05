import csv
import json
import os
import logging
from locust import FastHttpUser, TaskSet, task, between, run_single_user
import random

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Define the absolute path for the config file
config_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../config.json')
# Define the absolute path for the CSV data file
config_data_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/csv/post_activities.csv')
# Define the absolute path for the JSON data file
config_data_json = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../src/data/json/activities.json')

# Read the configuration file
with open(config_path, mode='r') as config_file:
    config = json.load(config_file)


class PostActivities(TaskSet):
    def on_start(self):
        # Read the CSV data file and store activities in a list
        self.activities = []
        with open(config_data_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.activities.append(row)

        # Read the JSON data file to get the base payload
        with open(config_data_json, mode='r') as file:
            self.base_payload = json.load(file)

    @task
    def post_activities(self):
        # Select a random activity from the list
        if self.activities:  # Verify if there are activities loaded
            # Choose a random activity
            activity = random.choice(self.activities)
            # Create a payload based on the base payload
            payload = self.base_payload.copy()  # Make a copy to avoid modifying the original
            # Change the title to the selected activity's title
            payload['title'] = activity['title']
            # Change the completed status based on the CSV value
            payload['completed'] = activity['completed'] == 'True'

            response = self.client.post(
                "/api/v1/Activities", json=payload
            )
            # Register the response details in the log
            logging.info(f"Status Code: {response.status_code}")
            logging.info(f"Response Body: {response.text}")


class WebsiteUser(FastHttpUser):
    # Define the base URL from the config
    host = config['base_url']
    tasks = [PostActivities]
    wait_time = between(1, 5)


if __name__ == "__main__":
    run_single_user(PostActivities)
