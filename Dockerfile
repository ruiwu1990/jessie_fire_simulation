FROM nvidia/cuda:latest
MAINTAINER Rui Wu
LABEL description="Parts of this docker file is from nvidia/cuda image."

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential cmake gdal-bin libgdal-dev

ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

#copy source code
COPY . /fire_sim
WORKDIR /fire_sim
ENV PYTHONPATH /var/www/fire_sim

#build fire lib
RUN rm -rf /fire_sim/fire_sim_lib/build/* \ 
    && cd /fire_sim/fire_sim_lib/build \ 
    && cmake .. \ 
    && make

#install requirements
RUN pip install -r requirements.txt

EXPOSE 5000
ENV FIRE_PORT 80
ENV FIRE_HOST 0.0.0.0
EXPOSE ${FIRE_PORT}

CMD python views.py -p 5000 --threaded