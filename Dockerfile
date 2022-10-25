FROM python:3.10.8-buster

RUN apt-get update
RUN apt install -y libgl1-mesa-dev
RUN pip install opencv-python
