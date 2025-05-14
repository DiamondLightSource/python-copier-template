ARG PYTHON_VERSION=3.11
# Use same base image as debug to prevent incompatibilities 
FROM python:${PYTHON_VERSION}-slim

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install libnss-ldapd -y
COPY dls-nslcd.conf /etc/nslcd.conf

ENTRYPOINT [ "nslcd" ]
CMD [ "--debug" ]
