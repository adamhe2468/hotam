FROM python:3-alpine

COPY . /home
RUN pip3 install -r /home/requirements.txt

CMD python3 /home/server.py

