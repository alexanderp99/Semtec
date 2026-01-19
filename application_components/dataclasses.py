from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from typing import Union


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
        if not (0 <= self.value <= 300):
            raise ValueError(f"{self.__class__.__name__} value must be between 0 and 300. Got: {self.value}")
        self.name = "HeartRateMeasurement"
        self.measurement_type = MeasurementType.HEART_RATE_MEASUREMENT

    def __str__(self):
        return f"HeartRateMeasurement(value={self.value})"

    def __repr__(self):
        return f"HeartRateMeasurement(value={self.value})"


@dataclass
class InflammatoryMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (0 <= self.value <= 50):
            raise ValueError(f"{self.__class__.__name__} value must be between 0 and 50. Got: {self.value}")
        self.name = "InflammatoryMeasurement"
        self.measurement_type = MeasurementType.INFLAMMATORY_MEASUREMENT

    def __str__(self):
        return f"InflammatoryMeasurement(value={self.value})"

    def __repr__(self):
        return f"InflammatoryMeasurement(value={self.value})"


@dataclass
class GroundHardnessMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (1 <= self.value <= 10):
            raise ValueError(f"{self.__class__.__name__} value must be between 1 and 10. Got: {self.value}")
        self.name = "GroundHardnessMeasurement"
        self.measurement_type = MeasurementType.GROUND_HARDNESS_MEASUREMENT

    def __str__(self):
        return f"GroundHardnessMeasurement(value={self.value})"

    def __repr__(self):
        return f"GroundHardnessMeasurement(value={self.value})"


@dataclass
class EKGReadingMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (0 <= self.value <= 4):
            raise ValueError(f"{self.__class__.__name__} value must be between 0 and 4. Got: {self.value}")
        self.name = "EKGReadingMeasurement"
        self.measurement_type = MeasurementType.EKG_READING_MEASUREMENT

    def __str__(self):
        return f"EKGReadingMeasurement(value={self.value})"

    def __repr__(self):
        return f"EKGReadingMeasurement(value={self.value})"


@dataclass
class MuscleTensionMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (1 <= self.value <= 10):
            raise ValueError(f"{self.__class__.__name__} value must be between 1 and 10. Got: {self.value}")
        self.name = "MuscleTensionMeasurement"
        self.measurement_type = MeasurementType.MUSCLE_TENSION_MEASUREMENT

    def __str__(self):
        return f"MuscleTensionMeasurement(value={self.value})"

    def __repr__(self):
        return f"MuscleTensionMeasurement(value={self.value})"


@dataclass
class AirflowMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (0 <= self.value <= 1000):
            raise ValueError(f"{self.__class__.__name__} value must be between 0 and 1000. Got: {self.value}")
        self.name = "AirflowMeasurement"
        self.measurement_type = MeasurementType.AIRFLOW_MEASUREMENT

    def __str__(self):
        return f"AirflowMeasurement(value={self.value})"

    def __repr__(self):
        return f"AirflowMeasurement(value={self.value})"


@dataclass
class ChokingMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (1 <= self.value <= 10):
            raise ValueError(f"{self.__class__.__name__} value must be between 1 and 10. Got: {self.value}")
        self.name = "ChokingMeasurement"
        self.measurement_type = MeasurementType.CHOKING_MEASUREMENT

    def __str__(self):
        return f"ChokingMeasurement(value={self.value})"

    def __repr__(self):
        return f"ChokingMeasurement(value={self.value})"


@dataclass
class BreathingRateMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (0 <= self.value <= 60):
            raise ValueError(f"{self.__class__.__name__} value must be between 0 and 60. Got: {self.value}")
        self.name = "BreathingRateMeasurement"
        self.measurement_type = MeasurementType.BREATHING_RATE_MEASUREMENT

    def __str__(self):
        return f"BreathingRateMeasurement(value={self.value})"

    def __repr__(self):
        return f"BreathingRateMeasurement(value={self.value})"


@dataclass
class AsthmaAttackMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (1 <= self.value <= 10):
            raise ValueError(f"{self.__class__.__name__} value must be between 1 and 10. Got: {self.value}")
        self.name = "AsthmaAttackMeasurement"
        self.measurement_type = MeasurementType.ASTHMA_ATTACK_MEASUREMENT

    def __str__(self):
        return f"AsthmaAttackMeasurement(value={self.value})"

    def __repr__(self):
        return f"AsthmaAttackMeasurement(value={self.value})"


@dataclass
class HyperventilationMeasurement(HealthMeasurement):
    def __post_init__(self):
        if not (1 <= self.value <= 10):
            raise ValueError(f"{self.__class__.__name__} value must be between 1 and 10. Got: {self.value}")
        self.name = "HyperventilationMeasurement"
        self.measurement_type = MeasurementType.HYPERVENTILATION_MEASUREMENT

    def __str__(self):
        return f"HyperventilationMeasurement(value={self.value})"

    def __repr__(self):
        return f"HyperventilationMeasurement(value={self.value})"


@dataclass
class MeasurementScheduleItem:
    measurements: List[HealthMeasurement]
    duration: int  # Number of ticks

    def __str__(self):
        return f"MeasurementScheduleItem(measurements={self.measurements}, duration={self.duration})"
    
    def __repr__(self):
        return f"MeasurementScheduleItem(measurements={self.measurements}, duration={self.duration})"


@dataclass
class MeasurementSchedule:
    schedule_items: List[MeasurementScheduleItem]
    default_measurements: List[HealthMeasurement]

    def get_measurements_at_tick(self, tick: int) -> List[HealthMeasurement]:
        current_tick = 0
        for item in self.schedule_items:
            if current_tick <= tick < current_tick + item.duration:
                return item.measurements
            current_tick += item.duration
        return self.default_measurements

    def __str__(self):
        return f"MeasurementSchedule(items={len(self.schedule_items)}, default={self.default_measurements})"

    def __repr__(self):
        return f"MeasurementSchedule(items={self.schedule_items}, default={self.default_measurements})"


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
    measurement_schedule: Optional[MeasurementSchedule] = None
    declines_request: bool = False

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
        return f"EmergencyHelpResponse(responder_ssn={self.first_responder_ssn}, patient_ssn={self.patient_ssn}, help_accepted={self.help_accepted})"

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
class GraphData:
    edges: List[Edge]
    people: List[Person]

    def get_person_by_ssn(self, ssn: int) -> Person:
        for person in self.people:
            if person.ssn == ssn:
                return person

    def __str__(self):
        return f"GraphData(edges={len(self.edges)}, people={len(self.people)})"

    def __repr__(self):
        return f"GraphData(edges={self.edges}, people={self.people}"

@dataclass
class Simulation:
    """
    Configuration for the simulation runtime.

    Attributes:
        number_data_iterations (int): Controls the loop count for data generation. For each loop, data is generated for each person.Higher values mean longer simulations.
        timeout_factor (float): Multiplier for the timeout calculation to reduce the risk of timeouts.
    """
    number_data_iterations: int
    timeout_factor: float

@dataclass
class Scenario:
    name: str
    description: str
    graph: GraphData
    simulation: Simulation

@dataclass
class Scenarios:
    scenarios: List[Scenario]

    def get_scenario_by_name(self, name: str) -> Scenario:
        for scenario in self.scenarios:
            if scenario.name == name:
                return scenario
        raise Exception(f"Scenario with name {name} not found")
