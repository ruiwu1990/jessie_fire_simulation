This is a server for Jessie fire simulation in the backend. Andy and Chase are in charge of Unity part. Rui is in charge of python server part and the front-end simulation visualization.

# Quick Start:
The user needs to create a folder to download two repositories:
1) https://github.com/ruiwu1990/jessie_fire_simulation/tree/new_design_requirements
2) https://github.com/andyhsia/firesim/tree/rui_dev

To fufil all the requirements for the python server, you need to run:
```
sudo pip install -r requirements.txt
```

You can run the program by:
```
python views.py -h 134.197.40.40 -p 5000 --threaded
```

134.197.40.40 should be replaced with your machine ip address. The command is to set up a server with your machine
