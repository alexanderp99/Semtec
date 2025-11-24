from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from hidden.bus.bus import EventBus
from hidden.simulation.initial_graph_data_generator import generate_graph_data

from hidden.datastructures.datastructures import AddPersonRequest, AddNodeRequest, AddEdgeRequest, AddEmergencyRequest

app = FastAPI()
connections = []
simulation = None   # will be set from mymain.py
bus:EventBus = None   # will be set at runtime

def set_bus(b):
    global bus
    bus = b

@app.get("/graph")
def get_data():
    return generate_graph_data()

@app.get("/")
def index():
    with open("hidden/gui/index.html") as f:
        return HTMLResponse(f.read())


@app.post("/add_person")
async def add_person(person: AddPersonRequest):
    simulation.add_person(person)
    return {"status": "ok"}


@app.post("/add_node")
async def add_person(node: AddNodeRequest):
    simulation.add_node(node)
    return {"status": "ok"}


@app.post("/add_edge")
async def add_person(edge: AddEdgeRequest):
    simulation.add_edge(edge)
    return {"status": "ok"}


@app.post("/add_emergency")
async def add_emergency(emergency: AddEmergencyRequest):
    simulation.add_emergency(emergency)
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            data = await ws.receive_json()
            print("Client sent:", data)
            await bus.publish(data)
    except:
        connections.remove(ws)


async def push_event(event):
    dead = []
    for ws in connections:
        try:
            await ws.send_json({"type": event.__class__.__name__, **event.__dict__})
            print("Pushing event:", event)

        except:
            dead.append(ws)
    for ws in dead:
        connections.remove(ws)
