from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
from starlette.websockets import WebSocketDisconnect

from CytoscapeConverter import CytoscapeConverter
from pathlib import Path


class GUIServer:
    def __init__(self, simpy):
        self.simpy = simpy
        self.app = FastAPI(title="GUI Server")
        self.websocket_connections = []
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        async def read_root(request: Request):
            return {"service": "Gui", "status": "running"}

        @self.app.get("/simulation/start")
        def start_simulation():
            self.simpy.start_simulation()
            return {"status": "simulation_started"}

        @self.app.get("/simulation/watch")
        def watch():
            html_file_path = Path(__file__).parent / "index.html"
            html_content = ""
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                return HTMLResponse(content=html_content)


        @self.app.get("/graphdata")
        def get_graphdata():
            graphdata = self.simpy.graph_data
            return CytoscapeConverter.convert_to_json_object(graphdata)

        @self.app.get("/simulation/stop")
        async def stop_simulation():
            await self.simpy.stop()
            return {"status": "simulation_stopped"}

        @self.app.post("/treatment/request")
        async def request_treatment(treatment_data: dict):
            await self.simpy.handle_treatment_request(treatment_data)
            return {"status": "treatment_requested"}

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.websocket_connections.append(websocket)
            try:
                while True:
                    data = await websocket.receive_json()
                    await self.handle_gui_command(data)
            except WebSocketDisconnect:
                self.websocket_connections.remove(websocket)

    async def handle_gui_command(self, command: dict):
        command_type = command.get("type")
        if command_type == "start_simulation":
            await self.simpy.handle_simulation_control({
                "action": "start",
                "parameters": command.get("parameters", {})
            })
        elif command_type == "treatment_request":
            await self.simpy.handle_treatment_request(command)

    async def broadcast_to_clients(self, message: dict):
        for websocket in self.websocket_connections:
            try:
                await websocket.send_json(message)
            except:
                self.websocket_connections.remove(websocket)

    async def start(self):
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        server = uvicorn.Server(config)
        print("Starting GUI Server on port 8000")
        await server.serve()