FROM continuumio/miniconda3:latest

RUN apt update -y && \
    apt install curl -y && \
    apt install sshpass -y && \
    apt install vim -y

RUN conda install lxml -y
RUN pip install ansible-core=='2.17.4' &&  \
    pip install docx-mailmerge && \
    pip install paramiko==3.3.1 && \
    pip install jmespath

RUN ansible-galaxy collection install community.general
RUN ansible-galaxy collection install cisco.ios

WORKDIR /home