from application_components.dataclasses import *
from broadcaster import Broadcast
import simpy
import asyncio
import threading
from threading import Lock
import logging
import simpy.rt
logger = logging.getLogger(__name__)

REAL_TIME_FACTOR = 0.1

class Simpy:
    """
    Simulation Environment - The "Real World"
    
    This class uses the SimPy library to simulate the city environment, citizens, and time.
    It acts as the source of truth for:
    1.  Events: Emergencies occurring (sensor data generation).
    2.  Citizens: Their location, health status, and decisions (e.g., accepting/declining help).
    3.  Time: Managing the flow of time in the simulation.
    """
    def __init__(self, broadcast: Broadcast, loop):
        self.broadcast = broadcast
        self.loop = loop
        self.env = simpy.rt.RealtimeEnvironment(factor=REAL_TIME_FACTOR, strict=
                                                False)
        self.simulation_stopped_event = self.env.event()
        self._simulation_lock = Lock()
        self.simulation_thread = None
        self.graph_data: GraphData = None
        self.simulation_config: Simulation = None
        self.number_of_people = 0

    async def start(self):
        """
        Initializes the simulation environment by connecting to the broadcast bus 
        and starting the listener for incoming responder selection events.
        """
        await self.broadcast.connect()
        asyncio.create_task(self.listen_to_bus_messages())

    async def listen_to_bus_messages(self):
        async with self.broadcast.subscribe(channel=Channel.HEALTH_RESPONDER_SELECTED_MESSAGE) as subscriber:
            async for event in subscriber:
                message_content = event.message
                self._handle_health_responder_selected(message_content)


    def _handle_health_responder_selected(self, message: HealthResponderSelectedMessage):
        """
        Responder Decision Simulation.
        When a citizen is selected by Medicus, this method simulates their reaction.
        -   Checks if the simulated person is configured to 'decline' requests.
        -   Sends an EmergencyHelpResponse (Accepted/Declined) back to Medicus.
        """

        person_declines:bool = self.graph_data.get_person_by_ssn(message.responder_ssn).declines_request
        if message.allowed_to_decline and person_declines:
            asyncio.run_coroutine_threadsafe(
                self.broadcast.publish(channel=Channel.HEALTH_RESPONDER_RESPONSE, message=EmergencyHelpResponse(first_responder_ssn=message.responder_ssn,patient_ssn=message.patient_ssn,help_accepted=False)),
                self.loop
            )
        else:
            asyncio.run_coroutine_threadsafe(
                self.broadcast.publish(channel=Channel.HEALTH_RESPONDER_RESPONSE,
                                       message=EmergencyHelpResponse(first_responder_ssn=message.responder_ssn,
                                                                     patient_ssn=message.patient_ssn,
                                                                     help_accepted=True)),
                self.loop
            )
        self.stop()


    def run_simulation(self):
        self.env.process(self.simulation_loop())

        try:
            self.env.run(until=self.simulation_stopped_event)
        except Exception as e:
            logger.error("Exception occurred while running simulation ")

    def monitor_simulation_state(self):
        """
        Monitors the simulation time and enforces a timeout.
        The timeout is calculated based on the number of people, configured iterations, and a safety factor.
        If the simulation exceeds this time, it is forcibly stopped to prevent infinite loops.
        """
        yield self.env.timeout(1/REAL_TIME_FACTOR * self.number_of_people * self.simulation_config.number_data_iterations * self.simulation_config.timeout_factor)
        logging.warning(f"Stopping Simpy due to time timeout!")
        self.simulation_stopped_event.succeed()


    def start_simulation(self):
        """
        Triggers the start of the simulation.
        1. Publishes the initial graph state to the message bus (Channel.INIT).
        2. Starts the timeout monitor process.
        3. Spawns the main simulation loop in a separate thread.
        """
        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.INIT, message=self.graph_data),
            self.loop
        )
        self.env.process(self.monitor_simulation_state())

        self.simulation_thread = threading.Thread(target=self.run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()

    def stop(self):
        if not self.simulation_stopped_event.triggered:
            self.simulation_stopped_event.succeed()
        else:
            logger.debug("Attempted to stop simulation, but the stop event was already triggered.")


    def simulation_loop(self):
        """
        Main Simulation Loop.
        Iterates through time, triggering events for each person in the city.
        In this prototype, it triggers health sensor readings.
        """

        iteration_round: int = 0

        while True:
            logger.info(f"Simpy simulation round: {str(iteration_round)}")

            for eachPerson in self.graph_data.people:
                yield self.env.timeout(20)
                self.send_health_message(eachPerson, iteration_round)

            iteration_round += 1


    def send_health_message(self, person:Person, iteration_round: int):
        """
        Sensor Simulation.
        Simulates a wearable device sending health metrics to the central system (Medicus).
        Publishes a HEALTH_MEASUREMENT message to the bus.
        """
        measurements = person.measurements
        if person.measurement_schedule:
            measurements = person.measurement_schedule.get_measurements_at_tick(iteration_round)

        message:HealthMessage = HealthMessage(
                patient_ssn=person.ssn,
                patient_edge=person.target,
                measurements=measurements
        )

        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.HEALTH_MEASUREMENT, message=message),
            self.loop
        )

    def load_scenario(self, graph_data: GraphData, simulation_config: Simulation):
        """
        Loads a specific scenario into the simulation environment.
        
        Args:
            graph_data (GraphData): The physical layout (nodes/edges) and people.
            simulation_config (Simulation): Configuration parameters for simulation runtime/timeout.
        """
        self.graph_data = graph_data
        self.simulation_config = simulation_config
        self.number_of_people = len(self.graph_data.people)
        
        # Re-initialize environment
        self.env = simpy.rt.RealtimeEnvironment(factor=REAL_TIME_FACTOR, strict=False)
        self.simulation_stopped_event = self.env.event()


