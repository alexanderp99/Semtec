from graphGenerator import GraphGenerator
from new_dataclasses import *
from broadcaster import Broadcast
import simpy
import asyncio
import threading


class Simpy:
    def __init__(self, broadcast: Broadcast, loop):
        self.broadcast = broadcast
        self.loop = loop
        self.env = simpy.Environment()
        self.simulation_running = False
        self.simulation_thread = None
        self.graph_data:GraphData = GraphGenerator.generate_graph_data()

    async def start(self):
        await self.broadcast.connect()
        asyncio.create_task(self.listen_to_bus_messages())
        self.simulation_thread = threading.Thread(target=self.run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()

    async def listen_to_bus_messages(self):
        async with self.broadcast.subscribe(channel=Channel.HEALTH_RESPONDER_SELECTED_MESSAGE) as subscriber:
            async for event in subscriber:
                message_content = event.message
                self._handle_health_responder_selected(message_content)


    def _handle_health_responder_selected(self, message: HealthResponderSelectedMessage):

        person_declines:bool = self.graph_data.get_person_by_ssn(message.responder_ssn).declines
        if not self.simulation_running and (message.allowed_to_decline and person_declines):
            asyncio.run_coroutine_threadsafe(
                self.broadcast.publish(channel=Channel.HEALTH_RESPONDER_RESPONSE, message=EmergencyHelpResponse(first_responder_ssn=message.responder_ssn,patient_ssn=message.responder_ssn,help_accepted=False)),
                self.loop
            )
        else:
            self.simulation_running = False

    def run_simulation(self):
        self.env.process(self.simulation_loop())
        while True:
            try:
                self.env.step()
            except Exception:
                break

    def start_simulation(self):
        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.INIT, message=self.graph_data),
            self.loop
        )
        self.simulation_running = True

    def stop(self):
        self.simulation_running = False


    def simulation_loop(self):
        while True:
            if self.simulation_running:
                yield self.env.timeout(9000)

                for eachPerson in self.graph_data.people:
                    self.env.process(self.send_person_message(eachPerson))

            else:
                yield self.env.timeout(6000)

    def send_person_message(self, person:Person):
        delay = 1000
        yield self.env.timeout(delay)

        message:HealthMessage = HealthMessage(
                patient_ssn=person.ssn,
                measurements=person.measurements
        )

        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.HEALTH_MEASUREMENT, message=message),
            self.loop
        )
