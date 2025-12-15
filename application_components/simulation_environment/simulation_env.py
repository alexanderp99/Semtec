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
    def __init__(self, broadcast: Broadcast, loop, graphdata: GraphData):
        self.broadcast = broadcast
        self.loop = loop
        self.env = simpy.rt.RealtimeEnvironment(factor=REAL_TIME_FACTOR, strict=
                                                False)
        self.simulation_stopped_event = self.env.event()
        self._simulation_lock = Lock()
        self.simulation_thread = None
        self.graph_data: GraphData = graphdata
        self.number_of_people = len(self.graph_data.people)
        self.number_data_iterations = 3

    async def start(self):
        await self.broadcast.connect()
        asyncio.create_task(self.listen_to_bus_messages())

    async def listen_to_bus_messages(self):
        async with self.broadcast.subscribe(channel=Channel.HEALTH_RESPONDER_SELECTED_MESSAGE) as subscriber:
            async for event in subscriber:
                message_content = event.message
                self._handle_health_responder_selected(message_content)


    def _handle_health_responder_selected(self, message: HealthResponderSelectedMessage):

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
        yield self.env.timeout(1/REAL_TIME_FACTOR * self.number_of_people * self.number_data_iterations * 1.5)
        logging.warning(f"Stopping Simpy due to time timeout!")
        self.simulation_stopped_event.succeed()


    def start_simulation(self):
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

        iteration_round: int = 0

        while True:
            logger.info(f"Simpy simulation round: {str(iteration_round)}")

            for eachPerson in self.graph_data.people:
                yield self.env.timeout(20)
                self.send_health_message(eachPerson)

            iteration_round += 1


    def send_health_message(self, person:Person):
        message:HealthMessage = HealthMessage(
                patient_ssn=person.ssn,
                patient_edge=person.target,
                measurements=person.measurements
        )

        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.HEALTH_MEASUREMENT, message=message),
            self.loop
        )

