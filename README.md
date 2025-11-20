new_main.py starten

Schauen ob die services laufen:

GUI
> http://localhost:8000/

Medicus
> http://localhost:8001/ 

Wenn die Simulation gestartet wird, werden alle Daten (Graph layout usw) von Simpy generiert und an Medicus geschickt. 
Simpy sendet dann kontinuierlich Sensordaten
> http://localhost:8000/simulation/start


Bei refresh sieht man immer die aktuellen daten in simpy, visualisiert in einem graph
> http://localhost:8000/simulation/watch

