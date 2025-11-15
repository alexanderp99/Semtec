from graphGenerator import GraphGenerator
from new_dataclasses import *
from broadcaster import Broadcast
import simpy
import asyncio
import threading


class Simpy:
    def __init__(self, broadcast: Broadcast, loop, gui_server=None):
        self.broadcast = broadcast
        self.loop = loop
        self.gui_server = gui_server
        self.env = simpy.Environment()
        self.simulation_running = False
        self.simulation_thread = None
        self.pending_messages = simpy.Store(self.env)
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
                await self.handle_health_responder_selected(event)

    async def handle_health_responder_selected(self, message: HealthResponderSelectedMessageEnvelope):
        message_event = {
            'data': message,
            'simpy_event': simpy.Event(self.env)
        }
        self.pending_messages.put(message_event)
        try:
            await asyncio.to_thread(lambda: message_event['simpy_event'].result)
        except:
            pass

    async def handle_simulation_control(self, control_data: dict):
        message_event = {
            'data': {
                'type': 'simulation_control',
                'action': control_data.get('action'),
                'source': 'gui_direct'
            },
            'simpy_event': simpy.Event(self.env)
        }
        self.pending_messages.put(message_event)
        try:
            await asyncio.to_thread(lambda: message_event['simpy_event'].result)
        except:
            pass

    async def handle_treatment_request(self, treatment_data: dict):
        message_event = {
            'data': {
                'type': 'treatment_request',
                'patient_id': treatment_data.get('patient_id'),
                'treatment_type': treatment_data.get('treatment_type', 'standard'),
                'source': 'gui_direct'
            },
            'simpy_event': simpy.Event(self.env)
        }
        self.pending_messages.put(message_event)
        try:
            await asyncio.to_thread(lambda: message_event['simpy_event'].result)
        except:
            pass

    def run_simulation(self):
        self.env.process(self.message_processor())
        self.env.process(self.simulation_loop())
        while True:
            try:
                self.env.step()
            except Exception:
                break

    def message_processor(self):
        while True:
            message_event = yield self.pending_messages.get()
            message = message_event['data']
            yield from self.process_message(message)
            message_event['simpy_event'].succeed()

    def process_message(self, message):
        msg_type = message.get('type')
        source = message.get('source')

        if msg_type == 'first_responder_selected_request':
            yield from self.handle_treatment_request_internal(message)
        elif msg_type == 'simulation_control':
            yield from self.handle_simulation_control_internal(message)

    def handle_treatment_request_internal(self, message:HealthResponderSelectedMessageEnvelope):

        decline_treatment = False

        response = FirstResponderResponseEnvelope(data=FirstResponderSelectedMessage(responder_id=message.data.responder_id,patient_id=message.data.patient_id,declined=decline_treatment))

        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.HEALTH_RESPONDER_RESPONSE, message=response),
            self.loop
        )

        """
        if message.get('source') == 'gui_direct' and self.gui_server:
            asyncio.run_coroutine_threadsafe(
                self.gui_server.broadcast_to_clients(response),
                asyncio.get_event_loop()
            )
        else:
            asyncio.run_coroutine_threadsafe(
                self.send_to_bus(response),
                asyncio.get_event_loop()
            )
        """

    def start_simulation(self):
        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.INIT, message=self.graph_data),
            self.loop
        )
        self.simulation_running = True

    def stop(self):
        self.simulation_running = False

    def handle_simulation_control_internal(self, message):
        action = message.get('action')
        if action == 'start':

            asyncio.run_coroutine_threadsafe(
                self.broadcast.publish(channel=Channel.INIT, message=graphMessage),
                self.loop
            )
            self.simulation_running = True

        elif action == 'stop':
            self.simulation_running = False

        response = {
            'type': 'simulation_control_response',
            'action': action,
            'success': True,
            'sim_time': self.env.now
        }

        # Send to GUI directly if it came from GUI
        if message.get('source') == 'gui_direct' and self.gui_server:
            asyncio.run_coroutine_threadsafe(
                self.gui_server.broadcast_to_clients(response),
                asyncio.get_event_loop()
            )
        # Send to bus if it came from Medicus
        else:
            asyncio.run_coroutine_threadsafe(
                self.send_to_bus(response),
                asyncio.get_event_loop()
            )

    def simulation_loop(self):
        while True:
            if self.simulation_running:
                yield self.env.timeout(5000)

                for eachPerson in self.graph_data.people:
                    self.env.process(self.send_person_message(eachPerson))

                """
                update = {
                    'sim_time': self.env.now,
                    'data': {'active': True}
                }
                if self.gui_server:
                    asyncio.run_coroutine_threadsafe(
                        self.gui_server.broadcast_to_clients(update),
                        asyncio.get_event_loop()
                    )
                asyncio.run_coroutine_threadsafe(
                    self.broadcast.publish(channel="simulation_updates", message=update),
                    asyncio.get_event_loop()
                )"""
            else:
                yield self.env.timeout(5000)

    def send_person_message(self, person:Person):
        delay = 500
        yield self.env.timeout(delay)

        message = HealthMessage(
                person_ssn=person.ssn,
                measurements=person.measurements
        )

        asyncio.run_coroutine_threadsafe(
            self.broadcast.publish(channel=Channel.RESPONSES, message=message),
            self.loop
        )

    async def send_to_bus(self, response_data):
        response_data['source'] = 'simpy'
        await self.broadcast.publish(channel=Channel.RESPONSES, message=response_data)