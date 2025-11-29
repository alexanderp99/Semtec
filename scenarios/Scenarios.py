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
            measurements=[GroundHardnessMeasurement(value=4)]
        ),
        Person(
            target="e2",
            ssn=1,
            name="Matija",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.BASIC,
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
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]

    scenario = Scenario(name="Scenario 1", description="?", graph=GraphData(edges=edges,
                                                                            people=people))
    scenarios.append(scenario)

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
            measurements=[GroundHardnessMeasurement(value=4)]
        ),
        Person(
            target="e2",
            ssn=1,
            name="Matija",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.INTERMEDIATE,
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
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]
    scenario = Scenario(name="Scenario 2", description = "?", graph=GraphData(edges=edges,
        people=people))
    scenarios.append(scenario)

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
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.INTERMEDIATE,
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
            measurements=[InflammatoryMeasurement(value=20), GroundHardnessMeasurement(value=8)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]
    scenario = Scenario(name="Scenario 3", description="?", graph=GraphData(edges=edges,
                                                                            people=people))
    scenarios.append(scenario)

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
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.INTERMEDIATE,
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
            measurements=[InflammatoryMeasurement(value=21), GroundHardnessMeasurement(value=10)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]

    scenario = Scenario(name="Scenario 4", description="?", graph=GraphData(edges=edges,
                                                                            people=people))
    scenarios.append(scenario)

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
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.INTERMEDIATE,
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
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]

    scenario = Scenario(name="Scenario 5", description="?", graph=GraphData(edges=edges,
                                                                            people=people))
    scenarios.append(scenario)

    people = [
        Person(
            target="e0",
            ssn=0,
            name="Alex",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e2",
            ssn=1,
            name="Matija",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.BASIC,
            medicalHistory=None,
            measurements=[GroundHardnessMeasurement(value=4)]
        ),
        Person(
            target="e3",
            ssn=2,
            name="Rohit",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            declines_request=True,
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]

    scenario = Scenario(name="Scenario 6", description="?", graph=GraphData(edges=edges,
                                                                            people=people))
    scenarios.append(scenario)

    people = [
        Person(
            target="e0",
            ssn=0,
            name="Alex",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=[MedicalHistory(note="Broke left ankle", emergencyType="TraumaEmergency")],
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e2",
            ssn=1,
            name="Matija",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.BASIC,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e3",
            ssn=2,
            name="Rohit",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            declines_request=True,
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.RESPIRATORY,
            certificationLevel=CertificationLevel.ADVANCED,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]

    scenario = Scenario(name="Scenario 7", description="NO EVENT", graph=GraphData(edges=edges,
                                                                            people=people))
    scenarios.append(scenario)


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
            measurements=[HeartRateMeasurement(value=141), EKGReadingMeasurement(value=4),
                          BreathingRateMeasurement(value=7)],
        ),
        Person(
            target="e2",
            ssn=1,
            name="Matija",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.TRAUMA,
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
            measurements=[HeartRateMeasurement(value=100)]
        ),
        Person(
            target="e4",
            ssn=3,
            name="Bob",
            hasEmergency=False,
            type="FirstResponder",
            speciality=IllnessType.CARDIAC,
            certificationLevel=CertificationLevel.INTERMEDIATE,
            medicalHistory=None,
            measurements=[HeartRateMeasurement(value=100)]
        ),
    ]

    scenario = Scenario(name="Scenario 9", description="?", graph=GraphData(edges=edges,
                                                                            people=people))
    scenarios.append(scenario)

    return Scenarios(scenarios=scenarios)