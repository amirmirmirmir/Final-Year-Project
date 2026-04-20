from locust import HttpUser, task, between

class WikiUser(HttpUser):
    # wait between 5-15 seconds between clicks
    wait_time = between(5, 15) 

    @task(10) # load a basic page that is likely to be read
    def load_homepage(self):
        self.client.get("/")

    @task(5) # load a standard article that is also likely to be read
    def read_normal_article(self):
        self.client.get("/index.php/Main_Page")

    @task(1) # once every while query something heavier from the database
    def hit_random_article(self):
        self.client.get("/index.php/Special:Random")