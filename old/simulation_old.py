from hidden import old
import requests


def send_alex_data(env):
    while True:
        #heart_rate = 140
        hardness = 4
        location = "Elm Street 5"

        """requests.put(
            "http://localhost:8080/rest/items/Alex_HeartRate/state",
            headers={"Content-Type": "text/plain", "Accept": "application/json"},
            data=str(heart_rate)
        )"""
        requests.put(
            "http://localhost:8080/rest/items/Alex_HitGroundWithHardness/state",
            headers={"Content-Type": "text/plain", "Accept": "application/json"},
            data=str(hardness)
        )
        #requests.post("http://localhost:8080/rest/items/Alex_HitGroundWithHardness", data=str(hardness))
        #requests.post("http://localhost:8080/rest/items/Alex_Street_Location_Name", data=location)

        yield env.timeout(30)

env = old.Environment()
env.process(send_alex_data(env))
env.run(until=180)
