FROM ubuntu:14.04
MAINTAINER Conor Sullivan SullivanC@HoseMaster.com
RUN apt-get --yes --force-yes update
RUN apt-get install --yes --force-yes python-dev python-pip git
RUN mkdir ~/PythonScripts && cd ~/PythonScripts
RUN git clone https://github.com/conman1136/CanonCounts
RUN cd CanonCounts
RUN pip install -r requirements.txt
