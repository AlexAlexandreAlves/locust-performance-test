from locust import FastHttpUser, TaskSet, task, between


class PeopleBehavior(TaskSet):
    @task
    def get_people(self):
        self.client.get("/people")

    @task
    def get_starships(self):
        self.client.get("/starships")


class WebsiteUser(FastHttpUser):
    tasks = [PeopleBehavior]
    wait_time = between(1, 5)  # Tempo de espera entre as requisições
