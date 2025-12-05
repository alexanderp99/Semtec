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

    scenario = Scenario(name="Scenario 1", description="Basic Trauma Dispatch | Should select ssn 1", graph=GraphData(edges=edges,
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
    scenario = Scenario(name="Scenario 2", description = "Variation Basic Certification Required | Should select ssn 1", graph=GraphData(edges=edges,
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
            measurements=[InflammatoryMeasurement(value=20), GroundHardnessMeasurement(value=6)]
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
    scenario = Scenario(name="Scenario 3", description="Compound Fracture Trauma emergency | Should select ssn 1", graph=GraphData(edges=edges,
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
            measurements=[InflammatoryMeasurement(value=21), GroundHardnessMeasurement(value=9)]
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

    scenario = Scenario(name="Scenario 4", description="Toughest Compound Fracture Trauma Emergency | Should select ssn ", graph=GraphData(edges=edges,
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

    scenario = Scenario(name="Scenario 5", description="No emergency", graph=GraphData(edges=edges,
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

    scenario = Scenario(name="Scenario 6", description="Cardiac Arrest | Should select ssn 3", graph=GraphData(edges=edges,
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
            certificationLevel=CertificationLevel.BASIC,
            declines_request=True,
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

    scenario = Scenario(name="Scenario 7", description="Basic Trauma Dispatch Declined | Should select ssn 1, then 2", graph=GraphData(edges=edges,
                                                                                                people=people))
    scenarios.append(scenario)


    return Scenarios(scenarios=scenarios)