import asyncio
import uuid
import json
import requests
import uvicorn
from broadcaster import Broadcast
from fastapi import FastAPI
from flask import jsonify

from HealthMeasurementCategoriser import HealthMeasurementCategoriser
from new_dataclasses import *


class MedicusService:
    def __init__(self, broadcast: Broadcast,loop):
        self.broadcast = broadcast
        self.loop = loop
        self.app = FastAPI(title="Medicus API")
        self.websocket_connections = []
        self.setup_routes()
        self.GRAPHDB_BASE_URL = "http://localhost:7200"
        self.GRAPHDB_TOKEN = self.request_graphdb_auth_token()
        self.REPOSITORY_ID = "semtec"

    def request_graphdb_auth_token(self):
        url = f"{self.GRAPHDB_BASE_URL}/rest/login"
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

        return auth_token

    def setup_routes(self):
        @self.app.get("/")
        async def root():
            return {"service": "Medicus", "status": "running"}

    def _emergency_already_exists(self):
        return False

    def delete_patient_health_measurements(self, patient_ssn):
        replacement = {
            "ssn": str(patient_ssn)
        }
        query = self._load_query_template("./queries/delete_person_measurements.rq", replacement)
        self._insert_query(query)

    def notify_closest_responder(self):

        query = self._load_query_template("./queries/query_closest_responder.rq")
        #response = self._ask_query(query) TODO

        first_responder_id = 0
        responder_can_decline = True

        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(
                Channel.HEALTH_RESPONDER_SELECTED_MESSAGE,
                HealthResponderSelectedMessage(
                    patient_ssn=first_responder_id,
                    responder_ssn=first_responder_id,
                    allowed_to_decline=responder_can_decline
                )
            ),
            self.loop
        )

    async def start(self):
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=8001,
            log_level="info"
        )
        server = uvicorn.Server(config)

        asyncio.create_task(self.listen_to_events())

        print("Starting Medicus service on port 8001")
        await server.serve()

    async def listen_to_events(self):
        await asyncio.gather(
            self._listen_channel(Channel.INIT, self._add_graph_to_vectordatabase),
            self._listen_channel(Channel.HEALTH_RESPONDER_RESPONSE, self._handle_first_responder_response),
            self._listen_channel(Channel.HEALTH_MEASUREMENT, self._process_health_message)
        )

    async def _listen_channel(self, channel, handler):
        async with self.broadcast.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                handler(event.message)

    def _handle_first_responder_response(self, message: EmergencyHelpResponse):
        if message.help_accepted:
            patient_ssn = message.patient_ssn
            self.delete_patient_health_measurements(patient_ssn)
        else:
            replacements = {
                "ssn": message.patient_ssn,
                "emergency_id": "?"
            }
            query = self._load_query_template("./queries/insert_responder_declined.rq", replacements)
            self._insert_query(query)
            self.notify_closest_responder()

    def _process_health_message(self, data: HealthMessage):

        if self._emergency_already_exists():
            return

        replacements = HealthMeasurementCategoriser.process_measurements(data.measurements)

        for each_entry in replacements:
            query = self._load_query_template("./queries/insert_sensor_measurement.rq", each_entry.to_dict())
            self._insert_query(query)

        query = self._load_query_template("./queries/query_if_emergency.rq")
        # response = self._ask_query(query) TODO
        is_emergency = True

        if is_emergency:
            self.notify_closest_responder()
        else:
            self.delete_patient_health_measurements(data.patient_ssn)

    def _add_graph_to_vectordatabase(self, graph: GraphData):

        query = self._load_query_template("./queries/query_database_not_empty.rq")
        response = self._ask_query(query)

        elements_exist_in_database: bool = response[0]['boolean']

        if elements_exist_in_database:
            return # stop duplication
        else:
            for each_edge in graph.edges:
                self._insert_graph_edges(each_edge)

            for each_person in graph.people:
                self._insert_graph_person(each_person)

    def _insert_graph_edges(self, each_edge):

        replacements = each_edge.to_dict()
        query = self._load_query_template("./queries/insert_graph_edge.rq", replacements)
        self._insert_query(query)

    def _insert_graph_person(self, each_person):
        replacements = each_person.to_dict()
        replacements["id"] = str(uuid.uuid4())
        query = self._load_query_template("./queries/insert_graph_person.rq", replacements)
        self._insert_query(query)

    def _load_query_template(self, template_path, replacements=None):
        with open(template_path, 'r') as file:
            template = file.read()

        if replacements:
            for placeholder, value in replacements.items():
                template = template.replace(f"{{{placeholder}}}", value)

        return template

    def _insert_query(self, query):
        content_type = "application/sparql-update"
        return self._do_query_of_content_type(query, content_type=content_type)

    def _ask_query(self, query):
        content_type = "application/sparql-query"
        return self._do_query_of_content_type(query, content_type=content_type)

    def _do_query_of_content_type(self, query, content_type):
        headers = {
            "Content-Type": content_type,
            "Authorization": self.GRAPHDB_TOKEN
        }
        path = ""
        if "sparql-query" in content_type:
            path = f"{self.GRAPHDB_BASE_URL}/repositories/{self.REPOSITORY_ID}"
            headers["Accept"] = "application/sparql-results+json"
        elif "sparql-update" in content_type:
            path = f"{self.GRAPHDB_BASE_URL}/repositories/{self.REPOSITORY_ID}/statements"

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
