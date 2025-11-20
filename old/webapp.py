import dash
from dash import dcc, html, Input, Output
import json
from pathlib import Path
import requests

FASTAPI_URL = "http://127.0.0.1:8000"  # FastAPI service

app = dash.Dash(__name__)


BASE_DIR = Path(__file__).parent  # folder containing this script
template_path = BASE_DIR / "cytoscape_template.html"

template = template_path.read_text()


def fetch_graph():
    resp = requests.get(f"{FASTAPI_URL}")
    data = resp.json()
    return data


initial_graph = fetch_graph()


initial_html_content = template.replace("{{graph_data}}", json.dumps(initial_graph))

app.layout = html.Div([
    html.H1("Graph Visualization"),
    html.Iframe(
        id='graph-container',
        srcDoc=initial_html_content,
        style={'width': '100%', 'height': '500px', 'border': 'none'}
    )
])


@app.callback(
    Output('graph-container', 'srcDoc'),
)
def update_graph(n_clicks):
    graph = fetch_graph()
    elements = {
        "nodes": graph["nodes"],
        "edges": graph["edges"],
        "people": graph["people"],
    }
    html_content = template.replace("{{graph_data}}", json.dumps(elements))
    return html_content


if __name__ == '__main__':
    app.run(debug=False, port=8050)
