FROM ubuntu:14.04
MAINTAINER Conor Sullivan SullivanC@HoseMaster.com
RUN apt-get --yes --force-yes update
RUN apt-get install --yes --force-yes python-dev python-pip git
RUN mkdir /root/PythonScripts
RUN git clone https://github.com/conman1136/CanonCounts /root/PythonScripts/CanonCounts
RUN pip install -r /root/PythonScripts/CanonCounts/requirements.txt
ENTRYPOINT ["/root/PythonScripts/CanonCounts/Flask/run.py", "-D"]
