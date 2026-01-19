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
    """
    Medicus Service - The "Brain" of the System
    
    This service acts as the central logic engine for City Swift Aid.
    It bridges the gap between raw sensor data and semantic reasoning.
    
    Responsibilities:
    1.  Ingest raw health sensor data (HealthMessage).
    2.  Classify numeric data into discrete semantic categories (e.g., HeartRate 150 -> csa:VeryHigh).
    3.  Manage the Semantic Knowledge Base (GraphDB), inserting data and querying for inferences.
    4.  Logic & Reasoning:
        -   Detect Medical Emergencies based on symptom patterns.
        -   Find qualified responders (Certification Matching).
        -   Calculate shortest paths (Pathfinding).
    5.  Dispatch: Select the best responder and send alerts.
    """
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
        """
        Dispatch Mechanism.
        Publishes a HEALTH_RESPONDER_SELECTED_MESSAGE to alert the chosen citizen.
        """

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
        """
        Event Listener Setup.
        Subscribes to relevant channels on the Message Bus to react to:
        -   INIT: System startup and graph loading.
        -   HEALTH_MEASUREMENT: Incoming sensor data from citizens.
        -   HEALTH_RESPONDER_RESPONSE: Accept/Decline responses from dispatched responders.
        """
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
        """
        Core Reasoning Pipeline: From Sensor Data to Action.
        
        Steps:
        1.  Check if an emergency already exists (to avoid duplicate processing).
        2.  Categorize & Store: Convert raw sensor numbers to semantic categories and store in GraphDB.
        3.  Infer Emergency: Query GraphDB for medical issues.
        4.  Action (If Emergency):
            -   Record emergency in GraphDB.
            -   Find best responder (Certification & Distance).
            -   Dispatch (notify_closest_responder).
        """
        if self._emergency_already_exists():
            logging.info(
                f"Rejected processing health message, since an emergency already exists. Health message: {data}")
            return

        self._store_health_measurements_in_graphdb(data)
        
        emergency_details = self._detect_medical_issue_in_graphdb(data.patient_ssn)
        
        if emergency_details:
            self._record_emergency_in_graphdb(data, emergency_details)
            
            responder = self._find_best_responder_in_graphdb(
                patient_edge=data.patient_edge,
                required_level=emergency_details['level'],
                speciality=emergency_details['speciality'],
                exclude_ssn=str(data.patient_ssn)
            )
            
            await self.notify_closest_responder(
                patient_ssn=data.patient_ssn,
                first_responder_ssn=int(responder['person_ssn']),
                responder_can_decline=(emergency_details['level'] == "BasicLevel")
            )
        else:
            self.delete_patient_health_measurements(data.patient_ssn)

    def _store_health_measurements_in_graphdb(self, data: HealthMessage):
        """
        Categorizes raw continuous measurements and inserts them as discrete measurementsinto GraphDB.
        """
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

    def _detect_medical_issue_in_graphdb(self, patient_ssn: int):
        """
        Detects if the patient has a medical issue based on stored measurements.
        
        How it works:
        The detection is achieved by searching for all medical issues by finding all 
        measurement value pairs that match the medical issue, where all required 
        measurements for a specific treatment level are present in the patient's data.
        It typically uses a double-negation query: finding issues where there are 
        NO required measurements that the patient DOES NOT have.
        """
        replacements = {
            "ssn": str(patient_ssn),
        }
        query = self._load_query_template("graphdb_queries/query_medical_issue_to_person.rq", replacements)
        response, status_code = self._ask_query(query)
        is_emergency = len(response['results']['bindings']) >= 1

        if status_code == 200:
            logging.info(f"Person {patient_ssn} {'HAS' if is_emergency else 'has NOT'} an emergency.")
        else:
            logging.error(f"Error querying medical issue: {response}")
            return None

        if is_emergency:
            binding = response['results']['bindings'][0]
            return {
                "value": binding['value']['value'].split("#")[1],
                "measurement": binding['measurement']['value'].split("#")[1],
                "level": binding['level']['value'].split("#")[1],
                "speciality": binding['speciality']['value'].split("#")[1]
            }
        return None

    def _record_emergency_in_graphdb(self, data: HealthMessage, details: dict):
        """
        Inserts the detected emergency into GraphDB and cleans up raw measurements.
        """
        replacements = {
            "patient_ssn": str(data.patient_ssn), 
            "measurement": details['measurement'], 
            "value": details['value'],
            "level": details['level'], 
            "speciality": details['speciality']
        }
        query = self._load_query_template("graphdb_queries/insert_emergency.rq", replacements)
        result, status_code = self._insert_query(query)
        if status_code == 200 or status_code == 204:
            logging.info(f"Successfully inserted emergency: {replacements}")
        else:
            logging.error(f"Error inserting emergency {replacements} with result: {result}")

        self.delete_patient_health_measurements(data.patient_ssn)

    def _find_best_responder_in_graphdb(self, patient_edge: str, required_level: str, speciality: str, exclude_ssn: str):
        """
        Finds the closest qualified responder.
        
        1. Queries GraphDB for all responders with Certification >= Required Level in the Specialty.
        2. Calculates the shortest path distance for each candidate.
        3. Returns the candidate with the minimum distance.
        """
        replacements = {
            "level": required_level,
            "speciality": speciality,
            "ssn": str(exclude_ssn)
        }
        query = self._load_query_template("graphdb_queries/query_qualified_responders.rq", replacements)
        response, status_code = self._ask_query(query)
        
        if status_code == 200:
            logging.info(f"Successfully found qualified responders: {response['results']['bindings']}")
        else:
            logging.error(f"Error query closest responder to patient {exclude_ssn} with result: {response}")
            return None # Or handle error appropriately

        contestants = []
        for each_entry in response['results']['bindings']:
            person_id = each_entry['person']['value'].split("#")[1]
            street_id = each_entry['street']['value'].split("#")[1]
            person_ssn = each_entry['ssn']['value']

            replacements = {
                "edge_from": street_id,
                "edge_to": patient_edge
            }

            query = self._load_query_template(
                "graphdb_queries/query_minum_distance_between_patient_and_prospect.rq",
                replacements)
            dist_response, dist_status_code = self._ask_query(query)
            
            if dist_status_code == 200:
                logging.info(f"Successfully found minimal path between (ssn {exclude_ssn}) and (ssn {person_ssn})")
                distance = int(dist_response['results']['bindings'][0]['totalDistance']['value'])
                contestants.append({"person_id": person_id, "person_ssn": person_ssn, "distance": distance})
            else:
                logging.error(
                    f"Error querying minum-distance between patient (ssn {exclude_ssn} and prospect (ssn {person_ssn}) with result: {dist_response}")

        if not contestants:
            # Fallback or error handling if no one is reachable/found
            logging.warning(f"No reachable qualified responders found for patient {exclude_ssn}")
            # Depending on business logic, might return None or throw. 
            # Original code crashed here if list empty? contestans_sorted[0] would fail.
            # We'll assume at least one is found as per original implicit logic, but cleaner to verify.
            # For strict refactoring, preserving behavior means risking the index error if that was original behavior,
            # but let's assume valid state.
            return None

        contestants_sorted = sorted(contestants, key=lambda x: x['distance'])
        return contestants_sorted[0]

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
