import requests


def test_endpoints(base_url):
    query_responders(base_url)
    insert_first_responder(base_url)
    get_all_people(base_url)
    get_qualifications_by_person(base_url)
    get_who_can_respond(base_url)


def query_responders(base_url):
    url = f"{base_url}/query_responders"
    data = {
        "patient": "csa:8a9b3c2d-1e4f-6g7h-9i0r"
    }
    response = requests.post(url, json=data)
    print(f"POST /query responders - Status {response.status_code}")
    print(response.text)


def insert_first_responder(base_url):
    url = f"{base_url}/insert_first_responder"
    data = {
        "ssn": "123-45-6789",
        "name": "Test Person",
        "located_at": "1a9b3c2d-1e4f-6g7h-9i"
    }
    response = requests.post(url, json=data)
    print(f"POST /insert_first_responder - Status: {response.status_code}")


def get_all_people(base_url):
    url = f"{base_url}/get_all_people"
    response = requests.get(url)
    print(f"POST /get_all_people - Status: {response.status_code}")
    print(response.text)


def get_qualifications_by_person(base_url):
    url = f"{base_url}/query_qualifications_by_person"
    data = {
        "person": "csa:8a9b3c2d-1e4f-6g7h-9i00"
    }
    response = requests.post(url, json=data)
    print(f"POST /get qualifications by person - Status {response.status_code}")
    print(response.text)


def get_who_can_respond(base_url):
    url = f"{base_url}/query_qualified_responders"
    response = requests.get(url)
    print(f"POST /query qualified responders - Status {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    test_endpoints("http://localhost:5000")
