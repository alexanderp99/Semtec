import requests
import json
import logging
from flask import jsonify

logger = logging.getLogger(__name__)

class GraphDBClient:
    """
    Client for interacting with GraphDB.
    Encapsulates authentication and raw SPARQL query execution.
    """
    def __init__(self, base_url: str, repository_id: str, username: str = "admin", password: str = "root"):
        self.base_url = base_url
        self.repository_id = repository_id
        self.username = username
        self.password = password
        self.token = self._request_auth_token()

    def _request_auth_token(self):
        url = f"{self.base_url}/rest/login"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = {
            "username": self.username,
            "password": self.password
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            if response.status_code == 200:
                token = response.headers.get("authorization")
                if not token:
                     token = response.json().get('token') or response.text
                print(f"Successfully obtained token: {token}")
                return token
            else:
                print(f"Unexpected response: {response.status_code} - {response.text}")
                return ""

        except requests.exceptions.RequestException as e:
            print(f"Error obtaining token: {e}")
            return ""

    def insert_query(self, query: str):
        """Executes a SPARQL UPDATE (INSERT/DELETE) query."""
        content_type = "application/sparql-update"
        return self._do_query(query, content_type)

    def ask_query(self, query: str):
        """Executes a SPARQL QUERY (SELECT/ASK) query."""
        content_type = "application/sparql-query"
        return self._do_query(query, content_type)

    def _do_query(self, query: str, content_type: str):
        headers = {
            "Content-Type": content_type,
            "Authorization": self.token
        }
        path = ""
        if "sparql-query" in content_type:
            path = f"{self.base_url}/repositories/{self.repository_id}"
            headers["Accept"] = "application/sparql-results+json"
        elif "sparql-update" in content_type:
            headers["Accept"] = "*/*"
            path = f"{self.base_url}/repositories/{self.repository_id}/statements"

        try:
            response = requests.post(
                path,
                headers=headers,
                data=query.encode('utf-8')
            )

            try:
                # Handle empty responses (common for updates) vs JSON responses
                return_dic = {}
                if response.text and response.text.strip():
                     return_dic = json.loads(response.text)
                return return_dic, response.status_code
            except json.JSONDecodeError:
                # Fallback if response is text but not JSON
                return {}, response.status_code

        except Exception as e:
            logger.error(f"Connection to GraphDB failed: {e}")
            return {"error": str(e)}, 500
