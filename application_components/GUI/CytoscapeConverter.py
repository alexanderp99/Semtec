from application_components.dataclasses import *

class CytoscapeConverter:
    @staticmethod
    def convert_to_cytoscape(graph_data: GraphData) -> Dict[str, Any]:
        elements = []

        edge_nodes = set()
        for edge in graph_data.edges:
            edge_nodes.add(edge.id)
            edge_nodes.add(edge.target)

            elements.append({
                'data': {
                    'id': f"edge_{edge.id}",
                    'source': edge.id,
                    'target': edge.target,
                    'distance': edge.distance,
                    'label': f"{edge.distance}m"
                }
            })

        for node_id in edge_nodes:
            elements.append({
                'data': {
                    'id': node_id,
                    'label': node_id,
                    'type': 'edge_node'
                }
            })

        for person in graph_data.people:
            person_node_id = f"person_{person.ssn}"
            elements.append({
                'data': {
                    'id': person_node_id,
                    'label': person.name,
                    'type': person.type.lower(),
                    'ssn': person.ssn,
                    'speciality': person.speciality.value if hasattr(person.speciality, 'value') else str(
                        person.speciality),
                    'certification': person.certificationLevel.value if hasattr(person.certificationLevel,
                                                                                'value') else str(
                        person.certificationLevel),
                    'hasEmergency': person.hasEmergency
                }
            })

            elements.append({
                'data': {
                    'id': f"conn_{person.ssn}",
                    'source': person_node_id,
                    'target': person.target
                }
            })

        return {'elements': elements}

    @staticmethod
    def convert_to_json_object(graph_data: GraphData) -> Dict[str, Any]:
        cytoscape_data = CytoscapeConverter.convert_to_cytoscape(graph_data)
        return cytoscape_data