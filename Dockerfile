FROM debian:bullseye

RUN apt update
RUN apt install chromium=104.0.5112.101-1~deb11u1 -y
RUN apt-mark hold chromium
RUN apt install python3-pip -y

COPY . /src/fsj_webanalyser/
WORKDIR /src/fsj_webanalyser/

RUN pip install -r requirements.txt

CMD ["python3","./server.py"]