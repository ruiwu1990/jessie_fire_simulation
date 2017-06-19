This is a server for Jessie fire simulation in the backend. Andy and Chase are in charge of Unity part. Rui is in charge of python server part.


#Docker Quick Start
##Before You Start
1. You need to install the docker engine and here is the official link how to do it:
[Docker Engine Install Official link](https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository). 
The system has been tested with Docker version 17.03 and 17.05
2. All the server components should work if you have installed docker correctly.



You can run the program by:
```
docker run --name <container_name> -h 134.197.20.79 -p 5000:5000 ruiwu1990/jessie_fire_simulation:Dockerized python views.py
```

134.197.40.40 should be replaced with your machine ip address. The command is to set up a server with your machine
-p 5000:5000 means that mapping host machine port 5000 (first one) with docker container port 5000 (second one)

#Local Quick Start
##Before You Start
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

#Website URL
The system is available here
```
<Your IP>:5000/upload
```
For me the URL replaced with my ip is:
```
134.197.20.79:5000/upload
```