from application_components.dataclasses import *
from typing import List

def get_scenarios() -> Scenarios:
    scenarios: List[Scenario] = []

    edges = [
        Edge(id="e0", target="e1", distance=100),
        Edge(id="e1", target="e2", distance=150),
        Edge(id="e2", target="e3", distance=120),
        Edge(id="e3", target="e4", distance=180),
        Edge(id="e4", target="e5", distance=90),
        Edge(id="e5", target="e3", distance=200),
        Edge(id="e6", target="e5", distance=130)
    ]

    # --- Scenario 1: Basic Trauma Dispatch ---
    people_s1 = [
        Person(
            target="e0", ssn=0, name="Alex", hasEmergency=False, type="Citizen",
            speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
            measurements=[GroundHardnessMeasurement(value=1)],
            measurement_schedule=MeasurementSchedule(
                schedule_items=[
                    MeasurementScheduleItem(measurements=[GroundHardnessMeasurement(value=1)], duration=1),
                    MeasurementScheduleItem(measurements=[GroundHardnessMeasurement(value=4)], duration=1),
                ],
                default_measurements=[GroundHardnessMeasurement(value=1)]
            )
        ),
        Person(target="e2", ssn=1, name="Matija", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.BASIC, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e3", ssn=2, name="Rohit", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e4", ssn=3, name="Bob", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
    ]
    scenarios.append(Scenario(name="Scenario 1", description="Basic Trauma Dispatch | Alex triggers at tick 1", graph=GraphData(edges=edges, people=people_s1), simulation=Simulation(number_data_iterations=3, timeout_factor=1.5), goal_ssn_to_select=1))

    # --- Scenario 2: Variation Basic Certification Required ---
    people_s2 = [
        Person(
            target="e0", ssn=0, name="Alex", hasEmergency=False, type="Citizen",
            speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
            measurements=[GroundHardnessMeasurement(value=1)],
            measurement_schedule=MeasurementSchedule(
                schedule_items=[
                    MeasurementScheduleItem(measurements=[GroundHardnessMeasurement(value=1)], duration=1),
                    MeasurementScheduleItem(measurements=[GroundHardnessMeasurement(value=4)], duration=1),
                ],
                default_measurements=[GroundHardnessMeasurement(value=1)]
            )
        ),
        Person(target="e2", ssn=1, name="Matija", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.INTERMEDIATE, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e3", ssn=2, name="Rohit", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e4", ssn=3, name="Bob", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
    ]
    scenarios.append(Scenario(name="Scenario 2", description="Variation Basic Certification | Alex triggers at tick 1", graph=GraphData(edges=edges, people=people_s2), simulation=Simulation(number_data_iterations=3, timeout_factor=1.5), goal_ssn_to_select=1))

    # --- Scenario 3: Compound Fracture Trauma ---
    people_s3 = [
        Person(target="e0", ssn=0, name="Alex", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
               medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e2", ssn=1, name="Matija", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(
            target="e3", ssn=2, name="Rohit", hasEmergency=False, type="Citizen",
            speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[InflammatoryMeasurement(value=5), GroundHardnessMeasurement(value=2)],
            measurement_schedule=MeasurementSchedule(
                schedule_items=[
                    MeasurementScheduleItem(measurements=[InflammatoryMeasurement(value=5), GroundHardnessMeasurement(value=2)], duration=1),
                    MeasurementScheduleItem(measurements=[InflammatoryMeasurement(value=21), GroundHardnessMeasurement(value=9)], duration=1),
                ],
                default_measurements=[InflammatoryMeasurement(value=5), GroundHardnessMeasurement(value=2)]
            )
        ),
        Person(target="e4", ssn=3, name="Bob", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
    ]
    scenarios.append(Scenario(name="Scenario 3", description="Compound Fracture | Rohit triggers at tick 1", graph=GraphData(edges=edges, people=people_s3), simulation=Simulation(number_data_iterations=3, timeout_factor=1.5), goal_ssn_to_select=1))

    # --- Scenario 4: Toughest Compound Fracture ---
    people_s4 = [
        Person(target="e0", ssn=0, name="Alex", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
               medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e2", ssn=1, name="Matija", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(
            target="e3", ssn=2, name="Rohit", hasEmergency=False, type="Citizen",
            speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[InflammatoryMeasurement(value=5), GroundHardnessMeasurement(value=2)],
            measurement_schedule=MeasurementSchedule(
                schedule_items=[
                    MeasurementScheduleItem(measurements=[InflammatoryMeasurement(value=5), GroundHardnessMeasurement(value=2)], duration=1),
                    MeasurementScheduleItem(measurements=[InflammatoryMeasurement(value=21), GroundHardnessMeasurement(value=9)], duration=1),
                ],
                default_measurements=[InflammatoryMeasurement(value=5), GroundHardnessMeasurement(value=2)]
            )
        ),
        Person(target="e4", ssn=3, name="Bob", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
    ]
    scenarios.append(Scenario(name="Scenario 4", description="Toughest Compound Fracture | Rohit triggers at tick 1", graph=GraphData(edges=edges, people=people_s4), simulation=Simulation(number_data_iterations=3, timeout_factor=1.5), goal_ssn_to_select=1))

    # --- Scenario 5: No Emergency ---
    people_s5 = [
        Person(target="e0", ssn=0, name="Alex", hasEmergency=False, type="Citizen",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
               medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
               measurements=[HeartRateMeasurement(value=80)]), # Just normal heart rate
        Person(target="e2", ssn=1, name="Matija", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e3", ssn=2, name="Rohit", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e4", ssn=3, name="Bob", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.CARDIAC, certificationLevel=CertificationLevel.INTERMEDIATE, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
    ]
    scenarios.append(Scenario(name="Scenario 5", description="No Emergency | All constant normal", graph=GraphData(edges=edges, people=people_s5), simulation=Simulation(number_data_iterations=3, timeout_factor=1.5), goal_ssn_to_select=-1))

    # --- Scenario 6: Cardiac Arrest ---
    people_s6 = [
        Person(
            target="e0", ssn=0, name="Alex", hasEmergency=False, type="Citizen",
            speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
            measurements=[HeartRateMeasurement(value=80)], # Alex is the patient, but the emergency is cardiac, so initial measurement is normal HR
            measurement_schedule=MeasurementSchedule(
                schedule_items=[
                    MeasurementScheduleItem(measurements=[HeartRateMeasurement(value=80)], duration=1),
                    MeasurementScheduleItem(measurements=[HeartRateMeasurement(value=141), EKGReadingMeasurement(value=4), BreathingRateMeasurement(value=7)], duration=1),
                ],
                default_measurements=[HeartRateMeasurement(value=80)]
            )
        ),
        Person(target="e2", ssn=1, name="Matija", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.BASIC,
               medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e3", ssn=2, name="Rohit", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e4", ssn=3, name="Bob", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.CARDIAC, certificationLevel=CertificationLevel.INTERMEDIATE, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
    ]
    scenarios.append(Scenario(name="Scenario 6", description="Cardiac Arrest | Alex triggers at tick 1", graph=GraphData(edges=edges, people=people_s6), simulation=Simulation(number_data_iterations=3, timeout_factor=1.5), goal_ssn_to_select=3))

    # --- Scenario 7: Declined Dispatch ---
    people_s7 = [
        Person(
            target="e0", ssn=0, name="Alex", hasEmergency=False, type="Citizen",
            speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.BASIC,
            medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
            measurements=[GroundHardnessMeasurement(value=1)],
            measurement_schedule=MeasurementSchedule(
                schedule_items=[
                    MeasurementScheduleItem(measurements=[GroundHardnessMeasurement(value=1)], duration=1),
                    MeasurementScheduleItem(measurements=[GroundHardnessMeasurement(value=4)], duration=1),
                ],
                default_measurements=[GroundHardnessMeasurement(value=1)]
            )
        ),
        Person(target="e2", ssn=1, name="Matija", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.BASIC, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)], declines_request=True),
        Person(target="e3", ssn=2, name="Rohit", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.TRAUMA, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)]),
        Person(target="e4", ssn=3, name="Bob", hasEmergency=False, type="FirstResponder",
               speciality=IllnessType.RESPIRATORY, certificationLevel=CertificationLevel.ADVANCED, medicalHistory=None,
               measurements=[HeartRateMeasurement(value=80)])
    ]
    
    scenarios.append(Scenario(name="Scenario 7", description="Dispatch Declined | Alex triggers, Matija declines, Rohit accepts", graph=GraphData(edges=edges, people=people_s7), simulation=Simulation(number_data_iterations=3, timeout_factor=1.5), goal_ssn_to_select=2))


    return Scenarios(scenarios=scenarios)