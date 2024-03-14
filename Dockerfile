FROM python:3-alpine


COPY container-files/sshd_config /etc/ssh/
COPY container-files/entrypoint-alpine.sh ./entrypoint.sh
# Start and enable SSH
RUN apk add openssh \
    && echo "root:Docker!" | chpasswd \
    && chmod +x ./entrypoint.sh \
    && cd /etc/ssh/ \
    && ssh-keygen -A

COPY . /home
RUN pip3 install -r /home/requirements.txt

COPY container-files/sshd_config /etc/ssh/
ENTRYPOINT [ "./entrypoint.sh" ]


CMD python3 /home/server.py

