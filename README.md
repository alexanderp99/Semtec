Installierung

python -m ensurepip --upgrade
python -m pip install --upgrade setuptools
python -m pip install -r requirements.txt

Vorbereitung:
Graphdb starten
- Repository muss "semtec" heißen
- .pie aus "graphdb" entnehmen
- .ttl aus "graphdb" einfügen (Medical Issue concepts)


main.py starten

Schauen ob die services laufen:

GUI
> http://localhost:8000/
> http://localhost:8000/simulation/watch

Medicus
> http://localhost:8001/ 



Wenn die Simulation gestartet wird, werden alle Daten (Graph layout usw) von Simpy generiert und an Medicus geschickt. 
Simpy sendet dann kontinuierlich Sensordaten
> http://localhost:8000/simulation/start


Bei refresh sieht man immer die aktuellen daten in simpy, visualisiert in einem graph
> http://localhost:8000/simulation/watch




