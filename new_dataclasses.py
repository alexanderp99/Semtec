from dataclasses import dataclass, field
from enum import Enum
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
    CARDIAC = "CardiacSpeciality"
    TRAUMA = "TraumaSpeciality"
    NEUROLOGICAL = "NeurologicalSpeciality"
    RESPIRATORY = "RespiratorySpeciality"


class CertificationLevel(Enum):
    BASIC = "BasicLevel"
    INTERMEDIATE = "IntermediateLevel"
    ADVANCED = "AdvancedLevel"

    def to_json(self):
        return self.value


class Channel:
    HEALTH_MEASUREMENT = "health_measurement""simulation_responses"
    INIT = "simulation_init"
    HEALTH_RESPONDER_SELECTED_MESSAGE = "health_responder_selected_message"
    HEALTH_RESPONDER_RESPONSE = "health_responder_response"


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
    responder_ssn: int


class MeasurementType(Enum):
    HEART_RATE_MEASUREMENT = "HeartRateMeasurement"
    INFLAMMATORY_MEASUREMENT = "InflammatoryMeasurement"
    BREATHING_RATE_MEASUREMENT = "BreathingRateMeasurement"
    MUSCLE_TENSION_MEASUREMENT = "MuscleTensionMeasurement"
    CHOKING_MEASUREMENT = "ChokingMeasurement"
    ASTHMA_ATTACK_MEASUREMENT = "AsthmaAttackMeasurement"
    GROUND_HARDNESS_MEASUREMENT = "GroundHardnessMeasurement"
    EKG_READING_MEASUREMENT = "EKGReadingMeasurement"
    AIRFLOW_MEASUREMENT = "AirflowMeasurement"
    HYPERVENTILATION_MEASUREMENT = "HyperventilationMeasurement"

    def to_json(self):
        return self.value


@dataclass
class HealthMeasurement:
    value: Union[int, float]
    name: str = field(default="", init=False)
    measurement_type: MeasurementType = field(default=None, init=False)


@dataclass
class HeartRateMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "HeartRateMeasurement"
        self.measurement_type = MeasurementType.HEART_RATE_MEASUREMENT


@dataclass
class InflammatoryMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "InflammatoryMeasurement"
        self.measurement_type = MeasurementType.INFLAMMATORY_MEASUREMENT


@dataclass
class GroundHardnessMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "GroundHardnessMeasurement"
        self.measurement_type = MeasurementType.GROUND_HARDNESS_MEASUREMENT


@dataclass
class EKGReadingMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "EKGReadingMeasurement"
        self.measurement_type = MeasurementType.EKG_READING_MEASUREMENT


@dataclass
class MuscleTensionMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "MuscleTensionMeasurement"
        self.measurement_type = MeasurementType.MUSCLE_TENSION_MEASUREMENT


@dataclass
class AirflowMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "AirflowMeasurement"
        self.measurement_type = MeasurementType.AIRFLOW_MEASUREMENT


@dataclass
class ChokingMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "ChokingMeasurement"
        self.measurement_type = MeasurementType.CHOKING_MEASUREMENT


@dataclass
class BreathingRateMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "BreathingRateMeasurement"
        self.measurement_type = MeasurementType.BREATHING_RATE_MEASUREMENT


@dataclass
class AsthmaAttackMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "AsthmaAttackMeasurement"
        self.measurement_type = MeasurementType.ASTHMA_ATTACK_MEASUREMENT


@dataclass
class HyperventilationMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "HyperventilationMeasurement"
        self.measurement_type = MeasurementType.HYPERVENTILATION_MEASUREMENT


@dataclass
class HealthMeasurementValuePair:
    measurement_type: MeasurementType
    category: MeasurementCategory

    def to_dict(self):
        return {
            "measurement_type": self.measurement_type.value,
            "category": self.category.value,
        }


@dataclass
class Person:
    target: str
    ssn: int
    name: str
    hasEmergency: bool
    type: str
    speciality: IllnessType
    certificationLevel: CertificationLevel
    medicalHistory: Optional[List[MedicalHistory]] = None
    detectsEmergency: Optional[str] = None
    measurements: Optional[List[HealthMeasurement]] = None
    declines: bool = False

    def to_dict(self):
        return {
            "ssn": str(self.ssn),
            "target_location": self.target,
            "name": self.name,
            "has_emergency": str(self.hasEmergency).lower(),
            "person_type": self.type,
            "speciality": self.speciality.value,
            "certificationLevel": self.certificationLevel.value,
        }


@dataclass
class EmergencyHelpResponse:
    first_responder_ssn: int
    patient_ssn: int
    help_accepted: bool


@dataclass
class HealthMessage:
    patient_ssn: int
    patient_edge: str
    measurements: List[HealthMeasurement]


@dataclass
class HealthResponderSelectedMessage:
    patient_ssn: int
    responder_ssn: int
    allowed_to_decline: bool


@dataclass
class FirstResponderSelectedMessage:
    patient_ssn: int
    responder_ssn: int
    declined: bool


@dataclass
class GraphData:
    edges: List[Edge]
    people: List[Person]
    emergencies: List[Emergency]

    def get_person_by_ssn(self, ssn: int) -> Person:
        for person in self.people:
            if person.ssn == ssn:
                return person
