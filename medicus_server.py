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
    def __init__(self, broadcast: Broadcast, loop):
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

        query = self._load_query_template("./queries/query_if_emergency_exists.rq")
        response = self._ask_query(query)
        emergency_already_exists = response[0]['boolean']
        return emergency_already_exists

    def delete_patient_health_measurements(self, patient_ssn):
        replacement = {
            "ssn": str(patient_ssn)
        }
        query = self._load_query_template("./queries/delete_person_measurements.rq", replacement)
        self._insert_query(query)

    async def notify_closest_responder(self, patient_ssn, first_responder_ssn: int, responder_can_decline: bool):

        await self.broadcast.publish(
            Channel.HEALTH_RESPONDER_SELECTED_MESSAGE,
            HealthResponderSelectedMessage(
                patient_ssn=patient_ssn,
                responder_ssn=first_responder_ssn,
                allowed_to_decline=responder_can_decline
            )
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
                if asyncio.iscoroutinefunction(handler):
                    await handler(event.message)
                else:
                    handler(event.message)

    async def _handle_first_responder_response(self, message: EmergencyHelpResponse):
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
            await self.notify_closest_responder()

    async def _process_health_message(self, data: HealthMessage):

        if self._emergency_already_exists():
            return

        replacements = HealthMeasurementCategoriser.process_measurements(data.measurements)

        for each_entry in replacements:
            input = each_entry.to_dict() | {"ssn": str(data.patient_ssn)}
            query = self._load_query_template("./queries/insert_sensor_measurement.rq", input)
            self._insert_query(query)

        replacements = {
            "ssn": str(data.patient_ssn),
        }
        query = self._load_query_template("./queries/query_medical_issue_to_person.rq", replacements)
        response = self._ask_query(query)
        is_emergency = len(response[0]['results']['bindings']) >= 1

        if is_emergency:
            value = response[0]['results']['bindings'][0]['value']['value'].split("#")[1]
            measurement = response[0]['results']['bindings'][0]['measurment']['value'].split("#")[1]
            #treatment_level = response[0]['results']['bindings'][0]['treatmentLevel']['value']
            level: str = response[0]['results']['bindings'][0]['level']['value'].split("#")[1]
            speciality: str = response[0]['results']['bindings'][0]['speciality']['value'].split("#")[1]

            replacements = {"patient_ssn" : str(data.patient_ssn), "measurement":measurement, "value":value, "level":level, "speciality":speciality}
            query = self._load_query_template("./queries/insert_emergency.rq", replacements)
            self._insert_query(query)

            replacements = {
                "level": level,
                "speciality": speciality,
                "ssn": str(data.patient_ssn)
            }
            query = self._load_query_template("./queries/query_closest_responder.rq", replacements)
            response = self._ask_query(query)

            contestans = []
            for each_entry in response[0]['results']['bindings']:
                person_id = each_entry['person']['value'].split("#")[1]
                street_id = each_entry['street']['value'].split("#")[1]
                person_ssn = each_entry['ssn']['value']

                replacements = {
                    "edge_from": street_id,
                    "edge_to": data.patient_edge
                }

                query = self._load_query_template("./queries/query_minum_distance_between_patient_and_prospect.rq",
                                                  replacements)
                response = self._ask_query(query)

                distance = int(response[0]['results']['bindings'][0]['totalDistance']['value'])

                contestans.append({"person_id": person_id, "person_ssn": person_ssn, "distance": distance})

            can_decline: bool = False
            contestans_sorted = sorted(contestans, key=lambda x: x['distance'])
            selected_person = contestans_sorted[0]

            await self.notify_closest_responder(patient_ssn=data.patient_ssn,
                                                first_responder_ssn=int(selected_person["person_ssn"]),
                                                responder_can_decline=can_decline)
        else:
            self.delete_patient_health_measurements(data.patient_ssn)

    def _add_graph_to_vectordatabase(self, graph: GraphData):

        query = self._load_query_template("./queries/query_database_not_empty.rq")
        response = self._ask_query(query)

        elements_exist_in_database: bool = response[0]['boolean']

        if elements_exist_in_database:
            return  # stop duplication
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
            headers["Accept"] = "*/*"
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
