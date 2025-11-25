import asyncio
from medicus_server import MedicusService
from gui_server import GUIServer
from simulation_env import Simpy
from broadcaster import Broadcast
import logging
from scenarios import SimpleScenario

logging.basicConfig(level=logging.DEBUG)

async def main():
    broadcast = Broadcast("memory://")

    loop = asyncio.get_event_loop()

    simpy = Simpy(broadcast, loop=loop, graphdata=SimpleScenario.get_graph())
    gui_server = GUIServer(simpy)
    simpy.gui_server = gui_server
    medicus_service = MedicusService(broadcast,loop=loop)

    await asyncio.gather(
        gui_server.start(),  # Port 8000
        medicus_service.start(),  # Port 8001
        simpy.start(),
        return_exceptions=True
    )


if __name__ == "__main__":
    asyncio.run(main())