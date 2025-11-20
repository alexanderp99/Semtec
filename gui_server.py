from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from CytoscapeConverter import CytoscapeConverter


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

        @self.app.get("/simulation/stop")
        async def stop_simulation():
            await self.simpy.stop()
            return {"status": "simulation_stopped"}

        ## private
        @self.app.get("/graphdata")
        def get_graphdata():
            graphdata = self.simpy.graph_data
            return CytoscapeConverter.convert_to_json_object(graphdata)

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
