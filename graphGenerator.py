import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from new_dataclasses import *


class GraphGenerator:
    @staticmethod
    def generate_graph_data() -> GraphData:
        edges = [
            Edge(id="e0", target="e1", distance=100),
            Edge(id="e1", target="e2", distance=150),
            Edge(id="e2", target="e3", distance=120),
            Edge(id="e3", target="e4", distance=180),
            Edge(id="e4", target="e5", distance=90),
            Edge(id="e5", target="e3", distance=200),
            Edge(id="e6", target="e5", distance=130)
        ]

        people = [
            Person(
                target="e0",
                ssn=0,
                name="Alex",
                hasEmergency=False,
                type="FirstResponder",
                speciality=IllnessType.RESPIRATORY,
                certificationLevel=CertificationLevel.ADVANCED,
                medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
                measurements=[HeartRateMeasurement(value=100)]
            ),
            Person(
                target="e2",
                ssn=1,
                name="Matija",
                hasEmergency=False,
                type="Patient",
                speciality=IllnessType.RESPIRATORY,
                certificationLevel=CertificationLevel.ADVANCED,
                medicalHistory=None,
                measurements=[HeartRateMeasurement(value=100)]
            ),
            Person(
                target="e3",
                ssn=2,
                name="Rohit",
                hasEmergency=False,
                type="FirstResponder",
                speciality=IllnessType.RESPIRATORY,
                certificationLevel=CertificationLevel.ADVANCED,
                medicalHistory=None,
                measurements = [HeartRateMeasurement(value=100)]
            ),
            Person(
                target="e4",
                ssn=3,
                name="Bob",
                hasEmergency=False,
                type="Patient",
                speciality=IllnessType.RESPIRATORY,
                certificationLevel=CertificationLevel.ADVANCED,
                medicalHistory=None,
                measurements= [HeartRateMeasurement(value=100)]
            ),
        ]

        emergencies = [
        ]

        return GraphData(
            edges=edges,
            people=people,
            emergencies=emergencies
        )
