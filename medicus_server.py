import json
import uuid
from urllib import request

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import requests
from broadcaster import Broadcast
import uvicorn
import asyncio

from flask import jsonify

from HealthMeasurementCategoriser import HealthMeasurementCategoriser
from new_dataclasses import *
from graphGenerator import GraphGenerator

class MedicusService:
    def __init__(self, broadcast: Broadcast):
        self.broadcast = broadcast
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

        @self.app.post("/analyze")
        async def analyze_data(analysis_request: dict):
            await self.broadcast.publish("analysis_request", {
                "type": "medical_analysis",
                "data": analysis_request,
                "source": "medicus"
            })
            return {"status": "analysis_started", "request_id": "123"}

        @self.app.post('/data')
        def receive_data():
            content = request.json
            self._process_health_data(content)


    def _emergency_already_exists(self):
        return False

    def _process_health_data(self, data: HealthMessage):
        replacements = HealthMeasurementCategoriser.process_measurements(data.measurements)

        if self._emergency_already_exists():
            return

        for each_replacement in replacements:
            query = self._load_query_template("./queries/insert_sensor_measurement.rq", each_replacement)
            self._insert_query(query)

        person_id = data.person_id
        query = self._load_query_template("./queries/query_if_emergency.rq")
        response = self._ask_query(query)
        # response[0]['results']['bindings'][0]
        first_responder_id = ""
        responder_can_decline = True
        is_emergency = False

        if is_emergency:
            self.broadcast.publish(Channel.HEALTH_RESPONDER_SELECTED_MESSAGE,
                                   HealthResponderSelectedMessageEnvelope(data=HealthResponderSelectedMessage(patient_id=person_id,responder_id=first_responder_id,allowed_to_decline=responder_can_decline)))



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

        tasks = [
            self.listen_init_channel(),
            self.listen_health_measurements_channel(),
            self.listen_simulation_responses(),
        ]

        await asyncio.gather(*tasks)

    async def listen_init_channel(self):
        async with self.broadcast.subscribe(channel=Channel.INIT) as subscriber:
            async for event in subscriber:
                await self.handle_init_event(event)

    async def listen_health_measurements_channel(self):
        async with self.broadcast.subscribe(channel=Channel.UPDATES) as subscriber:
            async for event in subscriber:
                await self.handle_init_event(event)

    async def listen_simulation_responses(self):
        async with self.broadcast.subscribe(channel=Channel.RESPONSES) as subscriber:
            async for event in subscriber:
                await self.handle_simulation_responses_event(event)

    async def handle_simulation_responses_event(self, event):

        message_content = event.message
        self._process_health_data(message_content)

    async def handle_measurement_event(self, event):
        health_message = HealthMessage.from_json(event.message)

        self._process_health_data(health_message)

    async def handle_init_event(self, event):
        graph = event.message

        self._add_graph_to_vectordatabase(graph)


    def _add_graph_to_vectordatabase(self,graph: GraphData):

        for each_edge in graph.edges:
            self._insert_graph_edges(each_edge)

        for each_person in graph.people:
            self._insert_graph_person(each_person)

    def _insert_graph_edges(self, each_edge):

        replacements = each_edge.to_dict()
        query = self._load_query_template("./queries/insert_graph_edge.rq", replacements)
        self._insert_query(query)
        pass

    def _insert_graph_person(self, each_person):
        replacements = each_person.to_dict()
        replacements["id"] = str(uuid.uuid4())
        query = self._load_query_template("./queries/insert_graph_person.rq", replacements)
        self._insert_query(query)
        pass

    def _load_query_template(self, template_path, replacements):
        with open(template_path, 'r') as file:
            template = file.read()

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







