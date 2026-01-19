"""
City Swift Aid (CSA) - Main Orchestrator

This script serves as the entry point for the City Swift Aid Prototype.
It initializes and coordinates the four main architectural components:
1.  Message Bus (Broadcaster): Manages asynchronous communication between components.
2.  Simulation Environment (Simpy): Represents the "Real World" (City, Citizens, Sensors).
3.  GUI Server (FastAPI): Provides the visual interface (Cytoscape) to observe the simulation.
4.  Medicus Service (The "Brain"): The core logic engine handling semantic reasoning and dispatch.

Architecture:
    [Simulation] <--> [Message Bus] <--> [Medicus Service (Brain)]
         ^                                      |
         |                                      v
    [GUI Server]                           [GraphDB]
"""

import asyncio
from application_components.medicus.medicus_server import MedicusService
from application_components.GUI.gui_server import GUIServer
from application_components.simulation_environment.simulation_env import Simpy
from broadcaster import Broadcast
from scenarios.Scenarios import get_scenarios
import logging

#all_scenarios = [SimpleScenario.get_graph(), SimpleScenario2.get_graph()]

async def main():
    # 1. Initialize Message Bus
    # Uses an in-memory broadcast system for component communication
    broadcast = Broadcast("memory://")

    loop = asyncio.get_event_loop()

    # Load the specific test scenario (City Map, People, Emergency Types)
    selected_scenario = get_scenarios().get_scenario_by_name("Scenario 1")

    logging.basicConfig(level=logging.INFO,
                        handlers=[logging.FileHandler(f"scenario_{selected_scenario.name}.log", encoding='utf-8'), logging.StreamHandler()],
                        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    logger.info(f"Running scenario {selected_scenario.name}")

    # 2. Initialize Simulation Environment ("Real World")
    # Generates sensor data and handles responder acceptance/declines
    simpy = Simpy(broadcast, loop=loop)
    simpy.load_scenario(selected_scenario.graph, selected_scenario.simulation)
    
    # 3. Initialize GUI Server
    # Visualizes the city graph and simulation status
    gui_server = GUIServer(simpy)
    simpy.gui_server = gui_server
    
    # 4. Initialize Medicus Service ("The Brain")
    # Consumes sensor data, performs reasoning via GraphDB, and dispatches responders
    medicus_service = MedicusService(broadcast,loop=loop)
    medicus_service.reset_database()

    # Start all services concurrently
    await asyncio.gather(
        gui_server.start(),  # Port 8000
        medicus_service.start(),  # Port 8001
        simpy.start(),
        return_exceptions=True
    )


if __name__ == "__main__":
    asyncio.run(main())