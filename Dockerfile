FROM python:3.11-slim
MAINTAINER mokemokechicken@gmail.com

ENV PYTHONUNBUFFERED True

WORKDIR /tmp

RUN apt-get update
RUN apt-get -y install wget dpkg
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN apt-get -y install fonts-ipafont-gothic fonts-ipafont-mincho

ADD requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p /tmp/screenshot
WORKDIR /tmp/screenshot
ADD screenshot.py /tmp/

ENTRYPOINT ["python", "/tmp/screenshot.py"]
CMD ["--help"]
