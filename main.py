import asyncio
from application_components.medicus.medicus_server import MedicusService
from application_components.GUI.gui_server import GUIServer
from application_components.simulation_environment.simulation_env import Simpy
from broadcaster import Broadcast
from scenarios.Scenarios import get_scenarios
import logging

#all_scenarios = [SimpleScenario.get_graph(), SimpleScenario2.get_graph()]

async def main():
    broadcast = Broadcast("memory://")

    loop = asyncio.get_event_loop()

    selected_scenario = get_scenarios().get_scenario_by_name("Scenario 1")

    logging.basicConfig(level=logging.INFO,
                        handlers=[logging.FileHandler(f"scenario_{selected_scenario.name}.log", encoding='utf-8'), logging.StreamHandler()],
                        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    logger.info(f"Running scenario {selected_scenario.name}")

    simpy = Simpy(broadcast, loop=loop, graphdata=selected_scenario.graph)
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