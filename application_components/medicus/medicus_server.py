import asyncio
import uuid
import json
import requests
import uvicorn
from broadcaster import Broadcast
from fastapi import FastAPI
from flask import jsonify
import os
from pathlib import Path

from .HealthMeasurementCategoriser import HealthMeasurementCategoriser
from application_components.dataclasses import *
import logging

logger = logging.getLogger(__name__)
current_file = Path(__file__).resolve()


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

        query = self._load_query_template("graphdb_queries/query_if_emergency_exists.rq")
        response, status_code = self._ask_query(query)
        emergency_already_exists = response['boolean']
        return emergency_already_exists

    def delete_patient_health_measurements(self, patient_ssn):
        replacement = {
            "ssn": str(patient_ssn)
        }
        query = self._load_query_template("graphdb_queries/delete_person_measurements.rq", replacement)
        result, status_code = self._insert_query(query)
        if status_code == 200 or status_code == 204:
            logging.info(f"Successfully deleted health measurements of patient with ssn {patient_ssn}")
        else:
            logging.error(f"Error deleting health measurements: {status_code}, {result}")

    async def notify_closest_responder(self, patient_ssn, first_responder_ssn: int, responder_can_decline: bool):

        logging.info(
            f"First responder with ssn: {str(first_responder_ssn)} was chosen to help for patient ssn: {patient_ssn} and can delince: {responder_can_decline}")

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
            logger.info(f"Confirmed Selection of first responder with ssn {str(message.first_responder_ssn)}")
        else:
            replacements = {
                "ssn": str(message.patient_ssn),
                "emergency_id": "?"
            }
            query = self._load_query_template("graphdb_queries/insert_responder_declined.rq", replacements)
            result, status_code = self._insert_query(query)
            if status_code == 200 or status_code == 204:
                logging.info(
                    f"Successfully inserted, that potential first responder with ssn {str(message.first_responder_ssn)}, declined")
            else:
                logging.error(
                    f"Unsuccessfully tried inserting, that potential first responder with ssn {str(message.first_responder_ssn)}, declined ")
            await self.notify_closest_responder()

    async def _process_health_message(self, data: HealthMessage):

        if self._emergency_already_exists():
            logging.info(
                f"Rejected processing health message, since an emergency already exists. Health message: {data}")
            return

        replacements: List[HealthMeasurementValuePair] = HealthMeasurementCategoriser.process_measurements(
            data.measurements)
        logging.info(f"Health message: {data} was transformed into {replacements}")

        for each_entry in replacements:
            input = each_entry.to_dict() | {"ssn": str(data.patient_ssn)}
            query = self._load_query_template("graphdb_queries/insert_sensor_measurement.rq", input)
            result, status_code = self._insert_query(query)
            if status_code == 200 or status_code == 204:
                query_line = query.replace('\n', "")
                logging.info(f"Health message: {input} was successfully inserted as query {query_line}")
            else:
                logging.error(
                    f"Error inserting sensor measurement of person: {status_code} - {result}. Person ssn: {data.patient_ssn}. Measurement: {each_entry}")

        replacements = {
            "ssn": str(data.patient_ssn),
        }
        query = self._load_query_template("graphdb_queries/query_medical_issue_to_person.rq", replacements)
        response, status_code = self._ask_query(query)
        is_emergency = len(response['results']['bindings']) >= 1

        if status_code == 200:
            logging.info(f"Person {data.patient_ssn} {'HAS' if is_emergency else 'has NOT'} an emergency.")
        else:
            logging.error(f"Error querying medical issue: {response}")

        if is_emergency:
            value = response['results']['bindings'][0]['value']['value'].split("#")[1]
            measurement = response['results']['bindings'][0]['measurement']['value'].split("#")[1]
            # treatment_level = response['results']['bindings'][0]['treatmentLevel']['value']
            level: str = response['results']['bindings'][0]['level']['value'].split("#")[1]
            speciality: str = response['results']['bindings'][0]['speciality']['value'].split("#")[1]

            replacements = {"patient_ssn": str(data.patient_ssn), "measurement": measurement, "value": value,
                            "level": level, "speciality": speciality}
            query = self._load_query_template("graphdb_queries/insert_emergency.rq", replacements)
            result, status_code = self._insert_query(query)
            if status_code == 200 or status_code == 204:
                logging.info(f"Successfully inserted emergency: {replacements}")
            else:
                logging.error(f"Error inserting emergency {replacements} with result: {result}")

            self.delete_patient_health_measurements(data.patient_ssn)

            replacements = {
                "level": level,
                "speciality": speciality,
                "ssn": str(data.patient_ssn)
            }
            query = self._load_query_template("graphdb_queries/query_qualified_responders.rq", replacements)
            response, status_code = self._ask_query(query)
            if status_code == 200:
                logging.info(f"Successfully found qualified responders: {response['results']['bindings']}")
            else:
                logging.error(f"Error query closest responder to patient {data.patient_ssn} with result: {response}")

            contestans = []
            for each_entry in response['results']['bindings']:
                person_id = each_entry['person']['value'].split("#")[1]
                street_id = each_entry['street']['value'].split("#")[1]
                person_ssn = each_entry['ssn']['value']

                replacements = {
                    "edge_from": street_id,
                    "edge_to": data.patient_edge
                }

                query = self._load_query_template(
                    "graphdb_queries/query_minum_distance_between_patient_and_prospect.rq",
                    replacements)
                response, status_code = self._ask_query(query)
                if status_code == 200:
                    logging.info(
                        "Successfully found minimal path between (ssn {data.patient_ssn}) and (ssn {person_ssn})")
                else:
                    logging.error(
                        f"Error querying minum-distance between patient (ssn {data.patient_ssn} and prospect (ssn {person_ssn}) with result: {response}")

                distance = int(response['results']['bindings'][0]['totalDistance']['value'])

                contestans.append({"person_id": person_id, "person_ssn": person_ssn, "distance": distance})

            can_decline: bool = level == "BasicLevel"
            contestans_sorted = sorted(contestans, key=lambda x: x['distance'])
            selected_person = contestans_sorted[0]

            await self.notify_closest_responder(patient_ssn=data.patient_ssn,
                                                first_responder_ssn=int(selected_person["person_ssn"]),
                                                responder_can_decline=can_decline)
        else:
            self.delete_patient_health_measurements(data.patient_ssn)

    def _add_graph_to_vectordatabase(self, graph: GraphData):

        query = self._load_query_template("graphdb_queries/query_database_not_empty.rq")
        response, status_code = self._ask_query(query)

        elements_exist_in_database: bool = response['boolean']

        if elements_exist_in_database:
            logging.info(
                f"Rejected adding graph to vectordatabase, since it already has elements. Rejected graph: {graph} ")
            return
        else:
            for each_edge in graph.edges:
                self._insert_graph_edge(each_edge)

            for each_person in graph.people:
                self._insert_graph_person(each_person)

    def _insert_graph_edge(self, each_edge: Edge):

        replacements = each_edge.to_dict()
        query = self._load_query_template("graphdb_queries/insert_graph_edge.rq", replacements)
        result, status_code = self._insert_query(query)
        if status_code == 200 or status_code == 204:
            logging.info(f"Succesfully inserted graph edge: {each_edge}")
        else:
            logging.error(f"Failed to insert graph edge: {each_edge}")

    def delete_all_inserts(self):
        return

    def _insert_graph_person(self, each_person: Person):
        replacements = each_person.to_dict()
        replacements["id"] = str(uuid.uuid4())
        query = self._load_query_template("graphdb_queries/insert_graph_person.rq", replacements)
        result, status_code = self._insert_query(query)
        if status_code == 200 or status_code == 204:
            logging.info(f"Succesfully inserted graph person: {each_person}")
        else:
            logging.error(f"Failed to insert graph person: {each_person}")

    def _load_query_template(self, template_path, replacements=None):
        query_path = current_file.parent / template_path
        with open(query_path, 'r') as file:
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
