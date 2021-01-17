from locust import (
    HttpUser,
    TaskSet,
    task,
    between
)

HOST = "http://localhost:8000"
VOTING = 1

class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))

class DefAboutUs(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/aboutUs/")

class DefContactUs(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/contactUs/")


class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)

class AboutUs(HttpUser):
    host = HOST
    tasks = [DefAboutUs]
    wait_time = between(3,5)

class ContactUs(HttpUser):
    host = HOST
    tasks = [DefContactUs]
    wait_time = between(3,5)

