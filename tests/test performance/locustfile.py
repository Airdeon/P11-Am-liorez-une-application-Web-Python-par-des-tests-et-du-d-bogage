from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task(3)
    def display(self):
        self.client.get("/display")

    @task(3)
    def summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(3)
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")
