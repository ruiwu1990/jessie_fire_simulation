FROM nvidia/cuda
MAINTAINER Rui Wu

LABEL description="This Image builds a nvidia/cuda image."

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

#copy source code
COPY . /fire_sim
WORKDIR /fire_sim
ENV PYTHONPATH /var/www/fire_sim

#install requirements
RUN pip install -r requirements.txt


EXPOSE 5000
ENV FIRE_PORT 80
ENV FIRE_HOST 0.0.0.0
EXPOSE ${FIRE_PORT}

CMD python views.py -p 5000 --threaded