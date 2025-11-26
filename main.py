import asyncio
from application_components.medicus.medicus_server import MedicusService
from application_components.GUI.gui_server import GUIServer
from application_components.simulation_environment.simulation_env import Simpy
from broadcaster import Broadcast
from scenarios import SimpleScenario
import logging

logging.basicConfig(level=logging.INFO,handlers=[logging.FileHandler('scenario.log',encoding='utf-8'),logging.StreamHandler()],format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

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