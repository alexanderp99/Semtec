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
import time

AUTO_START_SIMULATION = True
# Scenarios to run in sequence
SCENARIOS_TO_RUN = ["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4", "Scenario 5", "Scenario 6", "Scenario 7"]

async def main():
    # 1. Initialize Message Bus
    broadcast = Broadcast("memory://")
    loop = asyncio.get_event_loop()
    
    # 2. Initialize Medicus Service ("The Brain")
    medicus_service = MedicusService(broadcast, loop=loop)
    
    # 3. Initialize GUI Server
    simpy = Simpy(broadcast, loop=loop)
    gui_server = GUIServer(simpy)
    simpy.gui_server = gui_server

    # Start Services
    # We start them once. They will persist across scenarios.
    gui_task = asyncio.create_task(gui_server.start())
    medicus_task = asyncio.create_task(medicus_service.start())
    simpy_task = asyncio.create_task(simpy.start())

    # Give services a moment to start
    await asyncio.sleep(2)

    scenarios = get_scenarios()
    selected_scenarios = [scenarios.get_scenario_by_name(name) for name in SCENARIOS_TO_RUN]

    for selected_scenario in selected_scenarios:
        # Re-configure logging for each scenario
        # Note: 'force=True' is needed to re-configure the root logger in Python 3.8+
        logging.basicConfig(level=logging.INFO,
                            handlers=[logging.FileHandler(f"scenario_{selected_scenario.name}.log", mode='w', encoding='utf-8'), logging.StreamHandler()],
                            format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            force=True)
        logger = logging.getLogger(__name__)

        logger.info(f"--- Starting Scenario: {selected_scenario.name} ---")

        # Reset Database
        medicus_service.reset_database()

        # Load Scenario into Simpy
        simpy.load_scenario(selected_scenario.graph, selected_scenario.simulation)

        if AUTO_START_SIMULATION:
            logger.info("Goal of ssn to select: " + str(selected_scenario.goal_ssn_to_select))
            simpy.start_simulation()
            
            # Wait for simulation to finish
            # We check if the simulation thread is alive.
            # When simulation calls self.stop(), the thread finishes.
            logger.info(f"Waiting for scenario {selected_scenario.name} to complete...")
            while simpy.simulation_thread and simpy.simulation_thread.is_alive():
                await asyncio.sleep(1)
            
            logger.info(f"--- Scenario {selected_scenario.name} Completed ---")
    
            
            # --- Result Verification ---
            if selected_scenario.goal_ssn_to_select != -1:
                log_file_name = f"scenario_{selected_scenario.name}.log"
                expected_phrase = f"Confirmed Selection of first responder with ssn {selected_scenario.goal_ssn_to_select}"
                
                try:
                    with open(log_file_name, 'r', encoding='utf-8') as f:
                        log_content = f.read()
                        
                    if expected_phrase in log_content:
                        logger.info(f"TEST PASSED: Found expected confirmation for SSN {selected_scenario.goal_ssn_to_select}")
                    else:
                        logger.error(f"TEST FAILED: Did not find '{expected_phrase}' in logs.")
                except Exception as e:
                    logger.error(f"TEST FAILED: Error reading log file for verification: {e}")
            else:
                logger.info("TEST SKIPPED: No goal SSN defined for this scenario.")

    logger.info("All scenarios completed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass