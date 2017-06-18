This is a server for Jessie fire simulation in the backend. Andy and Chase are in charge of Unity part. Rui is in charge of python server part.


#Docker Quick start
1. All the server components should be run in Ubuntu 16.04.
2. You need to install the docker engine and here is the official link how to do it:
[Docker Engine Install Official link](https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository). 
The system has been tested with Docker version 17.03 and 17.05
3. Install 



You can run the program by:
```
python views.py -h 134.197.40.40 -p 5000 --threaded
```

134.197.40.40 should be replaced with your machine ip address. The command is to set up a server with your machine


#Local Quick Start
First create a virtual environment
```
mkvirtualenv -p python2.7 dev
```

If you have created the virtual environment, then use this commend to enter it
```
virtualenv dev && source dev/bin/activate
```

Here is the command to install the requirements
```
pip install -r requirements.txt
```
Here is the command to set up and run the program
```
python views.py -h 134.197.20.79 -p 5000 --threaded
```
134.197.20.79 should be replaced with your machine ip address. The command is to set up a server with your machine