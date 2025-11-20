import asyncio

from flask import Flask, request, jsonify
import uuid
import requests
import json
from datetime import datetime

from hidden.bus.bus import EventBus
from hidden.datastructures.datastructures import NodeAdded, PersonAdded, EdgeAdded, EmergencyAdded

app = Flask(__name__)

bus:EventBus = None   # will be set at runtime
# GRAPHDB_BASE_URL = "http://graphdb:7200"
GRAPHDB_BASE_URL = "http://localhost:7200"
REPOSITORY_ID = "semtec"
GRAPHDB_TOKEN = ""

def initialize_bus_subscriptions():
    if bus is not None:
        asyncio.create_task(consume_bus_events())
        print("Bus subscriptions initialized")
    else:
        print("Warning: Cannot initialize subscriptions - bus is None")

async def consume_bus_events():
    try:
        async for event in bus.subscribe():  
            await on_bus_event(event)
    except Exception as e:
        print(f"Error in bus event consumption: {e}")

def set_bus(b):
    global bus
    bus = b
    initialize_bus_subscriptions()
@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/start")
def start():
    login(GRAPHDB_BASE_URL)
    return "started"


def insert_an_emergency(ssn: str, emergency_type: str):
    replacements = {
        "SSN": ssn
    }
    query = load_query_template("old_rq_statements/query_person_location.rq", replacements)

    response = ask_query(query)

    location_id = response[0]['results']['bindings'][0]['person']['value'].split("#")[1]
    patient_id = response[0]['results']['bindings'][0]['location']['value'].split("#")[1]

    ##create emergency
    emergency_id = f"Emergency{str(uuid.uuid4()).split('-')[0]}"
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    replacements = {
        "emergency_id": emergency_id,
        "patient_id": patient_id,
        "location_id": location_id,
        "emergency_type": emergency_type,
        "current_time": current_time
    }
    query = load_query_template("old_rq_statements/insert_emergency.rq", replacements)

    insert_response = insert_query(query)



@app.route('/data', methods=['POST'])
def receive_data():
    content = request.json
    if 'heartRate' in content:
        heart_rate = content.get('heartRate')
        heart_rate_unhealthy = heart_rate <= 30 or heart_rate >= 140
        if heart_rate_unhealthy:
            if heart_rate >= 140:
                insert_an_emergency(content.get('SSN'), "HeartAttack")
            else:
                insert_an_emergency(content.get('SSN'), "CardiacArrest")
    if 'hardness' in content:
        hardness = content.get('hardness')
        accident_occured = hardness >= 3
        if accident_occured:
            if hardness >= 6:
                insert_an_emergency(content.get('SSN'), "SimpleFracture")
            else:
                insert_an_emergency(content.get('SSN'), "CompoundFracture")



    print("Received from openHAB:", content)
    return '', 200


@app.route('/insert_first_responder', methods=['POST'])
def insert_a_person():
    data = request.json
    required_fields = ['ssn', 'name', 'located_at']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields (ssn, name, located_at)"}), 400

    ssn = data['ssn']
    name = data['name']
    located_at = data['located_at']

    person_uri = f"csa:{uuid.uuid4()}"

    replacements = {
        "person_uri": person_uri,
        "ssn": ssn,
        "name": name,
        "located_at": located_at
    }

    query = load_query_template("old_rq_statements/insert_first_responder.rq", replacements)

    return insert_query(query)


@app.route('/query_qualifications_by_person', methods=['POST'])
def query_qualifications_by_person():
    data = request.json
    required_fields = ['person']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields "}), 400

    person = data['person']

    replacements = {
        "person": person
    }

    query = load_query_template("old_rq_statements/query_qualifications_by_person.rq", replacements)

    return ask_query(query)


@app.route('/query_responders', methods=['POST'])
def query_responders():
    data = request.json
    required_fields = ['patient']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields (patient)"}), 400
    patient = data['patient']

    replacements = {
        "patient": patient
    }

    query = load_query_template("old_rq_statements/query_nearby_responders.rq", replacements)

    return ask_query(query)


def get_qualified_responders():
    replacements = {
    }
    query = load_query_template("old_rq_statements/query_qualified_responders.rq", replacements)

    return ask_query(query)


@app.route('/query_qualified_responders', methods=['GET'])
def query_qualified_responders():
    return get_qualified_responders()


@app.route('/get_all_people', methods=['GET'])
def get_all_people():
    replacements = {
    }

    query = load_query_template("old_rq_statements/query_all_people.rq", replacements)

    return ask_query(query)


def login(GRAPH_DB_BASE_URL):
    url = f"{GRAPH_DB_BASE_URL}/rest/login"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "username": "admin",
        "password": "root"
    }

    auth_token = ""

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        auth_token = response.headers["authorization"]

        if response.status_code == 200:
            token = response.json().get('token') or response.text
            print(f"Successfully obtained token: {token}")
        else:
            print(f"Unexpected response: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error obtaining token: {e}")

    global GRAPHDB_TOKEN
    GRAPHDB_TOKEN = auth_token


def insert_query(query):
    content_type = "application/sparql-update"
    return do_query_of_content_type(query, content_type=content_type)


def ask_query(query):
    content_type = "application/sparql-query"
    return do_query_of_content_type(query, content_type=content_type)


def do_query_of_content_type(query, content_type):
    headers = {
        "Content-Type": content_type,
        "Authorization": GRAPHDB_TOKEN
    }
    path = ""
    if "sparql-query" in content_type:
        path = f"{GRAPHDB_BASE_URL}/repositories/{REPOSITORY_ID}"
        headers["Accept"] = "application/sparql-results+json"
    elif "sparql-update" in content_type:
        path = f"{GRAPHDB_BASE_URL}/repositories/{REPOSITORY_ID}/statements"

    try:
        response = requests.post(
            path,
            headers=headers,
            data=query.encode('utf-8')
        )

        return_dic = {} if response.text == "" else json.loads(response.text)
        return return_dic, response.status_code

    except Exception as e:
        return jsonify({
            "error": "Connection to GraphDB failed",
            "details": str(e)
        }), 500


def load_query_template(template_path, replacements):
    with open(template_path, 'r') as file:
        template = file.read()

    for placeholder, value in replacements.items():
        template = template.replace(f"{{{placeholder}}}", value)

    return template

## new part

@app.route('/graph_nodes', methods=['POST'])
def add_graph_nodes():
    for each_node in request.json:
        add_graph_nodes(each_node)

@app.route('/graph_node', methods=['POST'])
def add_graph_node():
    replacements = {
        "node": "mynode",
    }
    query = load_query_template("graphdb_statements/insert_graph_node.rq", replacements)

    insert_response = insert_query(query)

@app.route('/graph_edges', methods=['POST'])
def add_graph_edges():
    for each_edge in request.json:
        add_graph_edges(each_edge)

@app.route('/graph_edge', methods=['POST'])
def add_graph_edge():
    replacements = {
        "edga": "myedge",
    }
    query = load_query_template("graphdb_statements/insert_graph_edge.rq", replacements)

    insert_response = insert_query(query)

@app.route('/first_responders', methods=['POST'])
def insert_first_responders():
    for each_first_responder in request.json:
        insert_first_responders(each_first_responder)

@app.route('/first_responder', methods=['POST'])
def insert_first_responder():
    data = request.json
    required_fields = ['ssn', 'name', 'located_at']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields (ssn, name, located_at)"}), 400

    ssn = data['ssn']
    name = data['name']
    located_at = data['located_at']

    person_uri = f"csa:{uuid.uuid4()}"

    replacements = {
        "person_uri": person_uri,
        "ssn": ssn,
        "name": name,
        "located_at": located_at
    }

    query = load_query_template("old_rq_statements/insert_first_responder.rq", replacements)

    return insert_query(query)

@app.route('/medical_emergency', methods=['POST'])
def insert_medical_emergency():

    ssn = request.json['ssn']
    emergency_type = request.json['emergency_type']
    replacements = {
        "SSN": ssn
    }
    query = load_query_template("old_rq_statements/query_person_location.rq", replacements)

    response = ask_query(query)

    location_id = response[0]['results']['bindings'][0]['person']['value'].split("#")[1]
    patient_id = response[0]['results']['bindings'][0]['location']['value'].split("#")[1]

    ##create emergency
    emergency_id = f"Emergency{str(uuid.uuid4()).split('-')[0]}"
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    replacements = {
        "emergency_id": emergency_id,
        "patient_id": patient_id,
        "location_id": location_id,
        "emergency_type": emergency_type,
        "current_time": current_time
    }
    query = load_query_template("old_rq_statements/insert_emergency.rq", replacements)

    insert_response = insert_query(query)

@app.route('/query_nearby_responders', methods=['POST'])
def query_nearby_responders():
    data = request.json
    required_fields = ['patient']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields (patient)"}), 400
    patient = data['patient']

    replacements = {
        "patient": patient
    }

    query = load_query_template("graphdb_statements/query_nearby_responders.rq", replacements)

    return ask_query(query)

STATEMENT_DIRECTORY = "graphdb_statements"

def insert_node(data):
    replacements = data
    query = load_query_template(STATEMENT_DIRECTORY + "/insert_graph_node.rq", replacements)

    insert_response = insert_query(query)


def insert_person(data):
    replacements = data
    query = load_query_template(STATEMENT_DIRECTORY + "/insert_person.rq", replacements)

    insert_response = insert_query(query)


def insert_edge(data):
    replacements = data
    query = load_query_template(STATEMENT_DIRECTORY + "/insert_edge.rq", replacements)

    insert_response = insert_query(query)


def insert_emergency(data):
    replacements = data
    query = load_query_template(STATEMENT_DIRECTORY + "/insert_emergency.rq", replacements)

    insert_response = insert_query(query)


async def on_bus_event(event):
    if isinstance(event, NodeAdded):
        print("Node added:", event.data)
        insert_node(event.data)
    elif isinstance(event, PersonAdded):
        print("Person added:", event.data)
        insert_person(event.data)
    elif isinstance(event, EdgeAdded):
        print("Edge added:", event.data)
        insert_edge(event.data)
    elif isinstance(event, EmergencyAdded):
        print("Emergency!", event.data)
        insert_emergency(event.data)


if __name__ == "__main__":
    app.run(host="localhost", port=5001)
