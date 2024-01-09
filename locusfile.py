from locust import HttpUser, task, between
import random

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def my_task(self):
        self.client.get("/tiles/photos/")

    @task
    def product_wall(self):
        list = ['Wall Tiles', 'Floor Tiles','Sanitary and CP Fittings','Granite and Marbles']
        pr = random.choice(list)
        self.client.get(f"/tiles/photos/?product={pr}")