# simulation/environment.py
import asyncio
from hidden.simulation.initial_graph_data_generator import generate_graph_data
from hidden.datastructures.datastructures import AddPersonRequest, PersonAdded, AddNodeRequest, NodeAdded, \
    AddEdgeRequest, EdgeAdded, EmergencyAdded, AddEmergencyRequest


class Simulation:
    def __init__(self, env, bus):
        self.env = env
        self.bus = bus

        # Load initial graph
        self.graph_data = generate_graph_data()
        self.nodes = self.graph_data["nodes"]
        self.edges = self.graph_data["edges"]
        self.people = self.graph_data["people"]

        env.process(self.run())

    def add_person(self, person: AddPersonRequest):
        self.people.append(person)
        asyncio.create_task(
            self.bus.publish(PersonAdded(time=self.env.now, data=person))
        )

    def add_node(self, node: AddNodeRequest):
        self.nodes.append(node)

        asyncio.create_task(
            self.bus.publish(NodeAdded(time=self.env.now, data=node))
        )

    def add_edge(self, edge: AddEdgeRequest):
        self.edges.append(edge)

        asyncio.create_task(
            self.bus.publish(EdgeAdded(time=self.env.now, data=edge))
        )

    def add_emergency(self, emergency: AddEmergencyRequest):
        self.edges.append(emergency)

        asyncio.create_task(
            self.bus.publish(EmergencyAdded(time=self.env.now, data=emergency))
        )

    def run(self):
        while True:
            yield self.env.timeout(1)
            # add logic to update graph dynamically

