# Running

> docker compose build
> docker compose create

Open http://localhost:7200/
> Create a repo named "semtec"
> Insert .pie named builtin_owl2-ql.pie
> Add rdf.ttl

Check if the app is up with http://localhost:5000/

Finally you HAVE to call this url http://localhost:5000/start such that the application established the connection to graphdb


## Testing

For testin use the "test_endpoints.py" file and just call it, all endpoints are executed.

## Simulation

> Use the /simpy/simulation script to make calls to openhab


## local installation and testing


Create venv

> python -m ensurepip --upgrade
> python -m pip install --upgrade setuptools
> python -m pip install --upgrade pip



