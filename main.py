# main.py
import asyncio
import simulation_env
import uvicorn
from hidden.bus.bus import EventBus
from hidden.microservice1 import set_bus as set_microservice_bus
from server import set_bus as set_server_bus
from hidden.simulation.simulation import Simulation
from hidden.util.FlaskThread import FlaskThread
from hidden.microservice1 import app
import server

async def simulation_task(bus):
    env = simpy.Environment()
    sim = Simulation(env, bus)
    server.simulation = sim
    while True:
        env.step()
        await asyncio.sleep(0)

async def consumer_task(bus):
    async for event in bus.subscribe():
        await server.push_event(event)

def start_flask(bus):
    set_microservice_bus(bus)
    set_server_bus(bus)
    t = FlaskThread(app)
    t.daemon = True
    t.start()
    return t

async def main():
    bus = EventBus()
    start_flask(bus)
    loop = asyncio.get_event_loop()
    loop.create_task(simulation_task(bus))
    loop.create_task(consumer_task(bus))
    config = uvicorn.Config("server:app", host="localhost", port=8000, log_level="info")
    server_instance = uvicorn.Server(config)
    await server_instance.serve()

if __name__ == "__main__":
    asyncio.run(main())
