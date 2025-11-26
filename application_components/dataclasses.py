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

    def __str__(self):
        return f"MessageType.{self.name}"

    def __repr__(self):
        return f"<MessageType.{self.name}: '{self.value}'>"


class MeasurementCategory(Enum):
    VERY_LOW = "VeryLow"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "VeryHigh"

    def to_json(self):
        return self.value

    def __str__(self):
        return f"MeasurementCategory.{self.name}"

    def __repr__(self):
        return f"<MeasurementCategory.{self.name}: '{self.value}'>"


class IllnessType(Enum):
    CARDIAC = "CardiacSpeciality"
    TRAUMA = "TraumaSpeciality"
    NEUROLOGICAL = "NeurologicalSpeciality"
    RESPIRATORY = "RespiratorySpeciality"

    def __str__(self):
        return f"IllnessType.{self.name}"

    def __repr__(self):
        return f"<IllnessType.{self.name}: '{self.value}'>"


class CertificationLevel(Enum):
    BASIC = "BasicLevel"
    INTERMEDIATE = "IntermediateLevel"
    ADVANCED = "AdvancedLevel"

    def to_json(self):
        return self.value

    def __str__(self):
        return f"CertificationLevel.{self.name}"

    def __repr__(self):
        return f"<CertificationLevel.{self.name}: '{self.value}'>"


class Channel:
    HEALTH_MEASUREMENT = "health_measurement""simulation_responses"
    INIT = "simulation_init"
    HEALTH_RESPONDER_SELECTED_MESSAGE = "health_responder_selected_message"
    HEALTH_RESPONDER_RESPONSE = "health_responder_response"

    def __str__(self):
        return f"Channel(class with constants: HEALTH_MEASUREMENT='{self.HEALTH_MEASUREMENT}', INIT='{self.INIT}')"

    def __repr__(self):
        return f"<Channel class>"


@dataclass
class TreatmentRequest:
    patient_ssn: int
    treatment_type: str = "standard"

    def __str__(self):
        return f"TreatmentRequest(patient_ssn={self.patient_ssn}, treatment_type='{self.treatment_type}')"

    def __repr__(self):
        return f"TreatmentRequest(patient_ssn={self.patient_ssn}, treatment_type='{self.treatment_type}')"


@dataclass
class SimulationControl:
    action: str

    def __str__(self):
        return f"SimulationControl(action='{self.action}')"

    def __repr__(self):
        return f"SimulationControl(action='{self.action}')"


@dataclass
class TreatmentResponse:
    patient_ssn: int
    success: bool
    processing_time: float
    sim_time: float

    def __str__(self):
        return f"TreatmentResponse(patient_ssn={self.patient_ssn}, success={self.success}, processing_time={self.processing_time:.2f}s, sim_time={self.sim_time:.2f})"

    def __repr__(self):
        return f"TreatmentResponse(patient_ssn={self.patient_ssn}, success={self.success}, processing_time={self.processing_time:.2f}, sim_time={self.sim_time:.2f})"


@dataclass
class SimulationControlResponse:
    action: str
    success: bool
    sim_time: float

    def __str__(self):
        return f"SimulationControlResponse(action='{self.action}', success={self.success}, sim_time={self.sim_time:.2f})"

    def __repr__(self):
        return f"SimulationControlResponse(action='{self.action}', success={self.success}, sim_time={self.sim_time:.2f})"


@dataclass
class SimulationUpdate:
    sim_time: float
    data: Dict[str, Any]

    def __str__(self):
        data_preview = str(self.data)[:50] + "..." if len(str(self.data)) > 50 else str(self.data)
        return f"SimulationUpdate(sim_time={self.sim_time:.2f}, data={data_preview})"

    def __repr__(self):
        return f"SimulationUpdate(sim_time={self.sim_time:.2f}, data={self.data})"


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

    def __str__(self):
        return f"Edge(id='{self.id}', target='{self.target}', distance={self.distance})"

    def __repr__(self):
        return f"Edge(id='{self.id}', target='{self.target}', distance={self.distance})"


@dataclass
class MedicalHistory:
    note: str
    emergencyType: str

    def __str__(self):
        return f"MedicalHistory(note='{self.note[:30]}...', emergencyType='{self.emergencyType}')"

    def __repr__(self):
        return f"MedicalHistory(note='{self.note}', emergencyType='{self.emergencyType}')"


@dataclass
class Emergency:
    responder_ssn: int

    def __str__(self):
        return f"Emergency(responder_ssn={self.responder_ssn})"

    def __repr__(self):
        return f"Emergency(responder_ssn={self.responder_ssn})"


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

    def __str__(self):
        return f"MeasurementType.{self.name}"

    def __repr__(self):
        return f"<MeasurementType.{self.name}: '{self.value}'>"


@dataclass
class HealthMeasurement:
    value: Union[int, float]
    name: str = field(default="", init=False)
    measurement_type: MeasurementType = field(default=None, init=False)

    def __str__(self):
        return f"HealthMeasurement(type={self.measurement_type}, value={self.value}, name='{self.name}')"

    def __repr__(self):
        return f"HealthMeasurement(value={self.value}, name='{self.name}', measurement_type={self.measurement_type})"


@dataclass
class HeartRateMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "HeartRateMeasurement"
        self.measurement_type = MeasurementType.HEART_RATE_MEASUREMENT

    def __str__(self):
        return f"HeartRateMeasurement(value={self.value})"

    def __repr__(self):
        return f"HeartRateMeasurement(value={self.value})"


@dataclass
class InflammatoryMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "InflammatoryMeasurement"
        self.measurement_type = MeasurementType.INFLAMMATORY_MEASUREMENT

    def __str__(self):
        return f"InflammatoryMeasurement(value={self.value})"

    def __repr__(self):
        return f"InflammatoryMeasurement(value={self.value})"


@dataclass
class GroundHardnessMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "GroundHardnessMeasurement"
        self.measurement_type = MeasurementType.GROUND_HARDNESS_MEASUREMENT

    def __str__(self):
        return f"GroundHardnessMeasurement(value={self.value})"

    def __repr__(self):
        return f"GroundHardnessMeasurement(value={self.value})"


@dataclass
class EKGReadingMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "EKGReadingMeasurement"
        self.measurement_type = MeasurementType.EKG_READING_MEASUREMENT

    def __str__(self):
        return f"EKGReadingMeasurement(value={self.value})"

    def __repr__(self):
        return f"EKGReadingMeasurement(value={self.value})"


@dataclass
class MuscleTensionMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "MuscleTensionMeasurement"
        self.measurement_type = MeasurementType.MUSCLE_TENSION_MEASUREMENT

    def __str__(self):
        return f"MuscleTensionMeasurement(value={self.value})"

    def __repr__(self):
        return f"MuscleTensionMeasurement(value={self.value})"


@dataclass
class AirflowMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "AirflowMeasurement"
        self.measurement_type = MeasurementType.AIRFLOW_MEASUREMENT

    def __str__(self):
        return f"AirflowMeasurement(value={self.value})"

    def __repr__(self):
        return f"AirflowMeasurement(value={self.value})"


@dataclass
class ChokingMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "ChokingMeasurement"
        self.measurement_type = MeasurementType.CHOKING_MEASUREMENT

    def __str__(self):
        return f"ChokingMeasurement(value={self.value})"

    def __repr__(self):
        return f"ChokingMeasurement(value={self.value})"


@dataclass
class BreathingRateMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "BreathingRateMeasurement"
        self.measurement_type = MeasurementType.BREATHING_RATE_MEASUREMENT

    def __str__(self):
        return f"BreathingRateMeasurement(value={self.value})"

    def __repr__(self):
        return f"BreathingRateMeasurement(value={self.value})"


@dataclass
class AsthmaAttackMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "AsthmaAttackMeasurement"
        self.measurement_type = MeasurementType.ASTHMA_ATTACK_MEASUREMENT

    def __str__(self):
        return f"AsthmaAttackMeasurement(value={self.value})"

    def __repr__(self):
        return f"AsthmaAttackMeasurement(value={self.value})"


@dataclass
class HyperventilationMeasurement(HealthMeasurement):
    def __post_init__(self):
        self.name = "HyperventilationMeasurement"
        self.measurement_type = MeasurementType.HYPERVENTILATION_MEASUREMENT

    def __str__(self):
        return f"HyperventilationMeasurement(value={self.value})"

    def __repr__(self):
        return f"HyperventilationMeasurement(value={self.value})"


@dataclass
class HealthMeasurementValuePair:
    measurement_type: MeasurementType
    category: MeasurementCategory

    def to_dict(self):
        return {
            "measurement_type": self.measurement_type.value,
            "category": self.category.value,
        }

    def __str__(self):
        return f"HealthMeasurementValuePair(measurement_type={self.measurement_type}, category={self.category})"

    def __repr__(self):
        return f"HealthMeasurementValuePair(measurement_type={self.measurement_type}, category={self.category})"


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

    def __str__(self):
        medical_history_count = len(self.medicalHistory) if self.medicalHistory else 0
        measurements_count = len(self.measurements) if self.measurements else 0
        return f"Person(ssn={self.ssn}, name='{self.name}', type='{self.type}', speciality={self.speciality}, location='{self.target}', hasEmergency={self.hasEmergency})"

    def __repr__(self):
        return f"Person(ssn={self.ssn}, name='{self.name}', type='{self.type}', speciality={self.speciality}, target='{self.target}', hasEmergency={self.hasEmergency}, certificationLevel={self.certificationLevel})"


@dataclass
class EmergencyHelpResponse:
    first_responder_ssn: int
    patient_ssn: int
    help_accepted: bool

    def __str__(self):
        status = "ACCEPTED" if self.help_accepted else "DECLINED"
        return f"EmergencyHelpResponse(responder_ssn={self.first_responder_ssn}, patient_ssn={self.patient_ssn}, status={status})"

    def __repr__(self):
        return f"EmergencyHelpResponse(first_responder_ssn={self.first_responder_ssn}, patient_ssn={self.patient_ssn}, help_accepted={self.help_accepted})"


@dataclass
class HealthMessage:
    patient_ssn: int
    patient_edge: str
    measurements: List[HealthMeasurement]

    def __str__(self):
        measurements_count = len(self.measurements)
        return f"HealthMessage(patient_ssn={self.patient_ssn}, patient_edge='{self.patient_edge}', measurements_count={measurements_count})"

    def __repr__(self):
        return f"HealthMessage(patient_ssn={self.patient_ssn}, patient_edge='{self.patient_edge}', measurements={self.measurements})"


@dataclass
class HealthResponderSelectedMessage:
    patient_ssn: int
    responder_ssn: int
    allowed_to_decline: bool

    def __str__(self):
        decline_status = "can decline" if self.allowed_to_decline else "cannot decline"
        return f"HealthResponderSelectedMessage(patient_ssn={self.patient_ssn}, responder_ssn={self.responder_ssn}, {decline_status})"

    def __repr__(self):
        return f"HealthResponderSelectedMessage(patient_ssn={self.patient_ssn}, responder_ssn={self.responder_ssn}, allowed_to_decline={self.allowed_to_decline})"


@dataclass
class FirstResponderSelectedMessage:
    patient_ssn: int
    responder_ssn: int
    declined: bool

    def __str__(self):
        status = "DECLINED" if self.declined else "SELECTED"
        return f"FirstResponderSelectedMessage(patient_ssn={self.patient_ssn}, responder_ssn={self.responder_ssn}, status={status})"

    def __repr__(self):
        return f"FirstResponderSelectedMessage(patient_ssn={self.patient_ssn}, responder_ssn={self.responder_ssn}, declined={self.declined})"


@dataclass
class GraphData:
    edges: List[Edge]
    people: List[Person]
    emergencies: List[Emergency]

    def get_person_by_ssn(self, ssn: int) -> Person:
        for person in self.people:
            if person.ssn == ssn:
                return person

    def __str__(self):
        return f"GraphData(edges={len(self.edges)}, people={len(self.people)}, emergencies={len(self.emergencies)})"

    def __repr__(self):
        return f"GraphData(edges={self.edges}, people={self.people}, emergencies={self.emergencies})"