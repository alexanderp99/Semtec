from enum import Enum
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from typing import Union


class MessageType(Enum):
    TREATMENT_REQUEST = "treatment_request"
    SIMULATION_CONTROL = "simulation_control"
    TREATMENT_RESPONSE = "treatment_response"
    SIMULATION_CONTROL_RESPONSE = "simulation_control_response"
    SIMULATION_UPDATE = "simulation_update"

    def to_json(self):
        return self.value

class MeasurementCategory(Enum):
    VERY_LOW = "VeryLow"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "VeryHigh"

    def to_json(self):
        return self.value

class IllnessType(Enum):
    CARDIAC = "cardiac"
    INFLAMMATORY = "inflammatory"
    RESPIRATORY = "respiratory"
    MUSCULAR = "muscular"

    def to_json(self):
        return self.value

class CertificationLevel(Enum):
    BASIC = "BasicLevel"
    INTERMEDIATE = "IntermediateLevel"
    ADVANCED = "AdvancedLevel"

    def to_json(self):
        return self.value


class Channel:
    COMMANDS = "simulation_commands"
    UPDATES = "simulation_updates"
    RESPONSES = "simulation_responses"
    INIT = "simulation_init"
    HEALTH_RESPONDER_SELECTED_MESSAGE = "health_responder_selected_message"
    HEALTH_RESPONDER_RESPONSE = "health_responder_response"

    def to_json(self):
        return self.value

@dataclass
class TreatmentRequest:
    patient_ssn: int
    treatment_type: str = "standard"

@dataclass
class SimulationControl:
    action: str

@dataclass
class TreatmentResponse:
    patient_ssn: int
    success: bool
    processing_time: float
    sim_time: float

@dataclass
class SimulationControlResponse:
    action: str
    success: bool
    sim_time: float

@dataclass
class SimulationUpdate:
    sim_time: float
    data: Dict[str, Any]

@dataclass
class Edge:
    id: str
    target: str
    distance: int

    def to_dict(self):
        return {
            "edge_id": self.id,
            "street_name": f"Edge {self.id}",
            "length": str(self.distance),
            "connected_to": self.target
        }

@dataclass
class MedicalHistory:
    note: str
    emergencyType: str


@dataclass
class Emergency:
    responder_ssn: str


@dataclass
class HealthMeasurement:
    value: Union[int, float]
    name: str = field(default="", init=False)

@dataclass
class Heartrate(HealthMeasurement):
    def __post_init__(self):
        self.name = "heartrate"

@dataclass
class Inflammatories(HealthMeasurement):
    def __post_init__(self):
        self.name = "inflammatories"

@dataclass
class BreathingRate(HealthMeasurement):
    def __post_init__(self):
        self.name = "breathingRate"

@dataclass
class MuscleTension(HealthMeasurement):
    def __post_init__(self):
        self.name = "muscleTension"

@dataclass
class Choking(HealthMeasurement):
    def __post_init__(self):
        self.name = "choking"

@dataclass
class AsthmaAttack(HealthMeasurement):
    def __post_init__(self):
        self.name = "asthmaAttack"

@dataclass
class GroundHardness(HealthMeasurement):
    def __post_init__(self):
        self.name = "groundHardness"

@dataclass
class EKGReading(HealthMeasurement):
    def __post_init__(self):
        self.name = "ekgReading"

@dataclass
class Airflow(HealthMeasurement):
    def __post_init__(self):
        self.name = "airflow"

@dataclass
class Hyperventilation(HealthMeasurement):
    def __post_init__(self):
        self.name = "hyperventilation"

@dataclass
class HealthMeasurementValuePair:
    illness_type: IllnessType
    category: MeasurementCategory

@dataclass
class Person:
    target: str
    ssn: str
    name: str
    hasEmergency: bool
    type: str
    speciality: IllnessType
    certificationLevel: CertificationLevel
    medicalHistory: Optional[List[MedicalHistory]] = None
    detectsEmergency: Optional[str] = None
    measurements: Optional[List[HealthMeasurement]] = None

    def to_dict(self):
        return {
            "ssn": self.ssn,
            "target_location": self.target,
            "name": self.name,
            "has_emergency": str(self.hasEmergency).lower(),
            "person_type": self.type,
            "speciality": self.speciality.value,
            "certificationLevel": self.certificationLevel.value,
        }

@dataclass
class HealthMessage:
    person_ssn: int
    measurements: List[HealthMeasurement]

    @classmethod
    def from_json(cls, json_str: str) -> 'HealthMessage':
        data = json.loads(json_str)
        return cls.from_dict(data)

@dataclass
class HealthMessageEnvelope:
    data: HealthMessage
    type: str = "HealthMessage"

@dataclass
class HealthResponderSelectedMessage:
    patient_ssn: str
    responder_ssn: str
    allowed_to_decline: bool

@dataclass
class FirstResponderSelectedMessage:
    patient_ssn: str
    responder_ssn: str
    declined: bool

@dataclass
class BusMessageEnvelope:
    type: str

@dataclass
class HealthResponderSelectedMessageEnvelope(BusMessageEnvelope):
    type: Channel.HEALTH_RESPONDER_SELECTED_MESSAGE
    data: HealthResponderSelectedMessage

@dataclass
class FirstResponderResponseEnvelope(BusMessageEnvelope):
    type: Channel.HEALTH_RESPONDER_RESPONSE
    data: FirstResponderSelectedMessage

@dataclass
class GraphData:
    edges: List[Edge]
    people: List[Person]
    emergencies: List[Emergency]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> 'GraphData':
        return cls(
            edges=[Edge(**edge) for edge in data['edges']],
            people=[Person(**person) for person in data['people']],
            emergencies=[Emergency(**emergency) for emergency in data['emergencies']]
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'GraphData':
        data = json.loads(json_str)
        return cls.from_dict(data)
