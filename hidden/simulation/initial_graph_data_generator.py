def generate_graph_data():
    nodes = [
        {"id": "n0", "label": "Node 0", "type": "typeA"},
        {"id": "n1", "label": "Node 1", "type": "typeB"},
        {"id": "n2", "label": "Node 2", "type": "typeC"},
        {"id": "n3", "label": "Node 3", "type": "typeA"},
        {"id": "n4", "label": "Node 4", "type": "typeB"},
        {"id": "n5", "label": "Node 5", "type": "typeC"}
    ]

    edges = [
        {"id": "e0", "source": "n0", "target": "n1", "distance": 100},
        {"id": "e1", "source": "n1", "target": "n2", "distance": 150},
        {"id": "e2", "source": "n2", "target": "n3", "distance": 120},
        {"id": "e3", "source": "n3", "target": "n4", "distance": 180},
        {"id": "e4", "source": "n4", "target": "n5", "distance": 90},
        {"id": "e5", "source": "n0", "target": "n3", "distance": 200},
        {"id": "e6", "source": "n2", "target": "n5", "distance": 130}
    ]

    people = [
        {
            "target": "e0",
            "name": "Alex",
            "hasEmergency": False,
            "type": "FirstResponder",
            "detectsEmergency": "TraumaEmergency",
            "certifications": ["AdvancedCardiacCertification", "IntermediateTraumaCertification"],
            "medicalHistory": [{"note": "Broke left ankle", "emergencyType": "TraumaEmergency"}]
        },
        {
            "target": "e2",
            "name": "Matija",
            "hasEmergency": False,
            "type": "Patient",
            "detectsEmergency": "TraumaEmergency",
            "certifications": ["BasicNeurologicalCertification", "AdvancedRespiratoryCertification"]
        },
        {
            "target": "e3",
            "name": "Rohit",
            "hasEmergency": False,
            "type": "FirstResponder",
            "certifications": ["FirstAidCertified"],
            "detectsEmergency": "TraumaEmergency"
        },
        {
            "target": "e4",
            "name": "Bob",
            "hasEmergency": False,
            "type": "Patient",
            "certifications": ["TraumaCareCertified"],
            "detectsEmergency": "TraumaEmergency"
        },
    ]

    emergencies = [
        {
            "responder_ssn":"0",

         }

    ]

    return {"nodes": nodes, "edges": edges, "people": people, "emergencies": emergencies}