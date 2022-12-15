FROM ubuntu:22.04

### install software
RUN apt-get update && apt-get install -y tzdata # avoid select timezone
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y python3-pip xinetd netcat
RUN python3 -m pip install pycryptodome

### user setting
ENV USER=ctf
ENV DIR=/home/${USER}

RUN groupadd -g 1000 ${USER} && \
    useradd -m -s /bin/bash -u 1000 -g 1000 ${USER}
RUN mkdir -p ${DIR}

### diretory setting
COPY --chown=root:${USER} start.sh /home/${USER}/start.sh
COPY --chown=root:${USER} ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:${USER} prob.py /home/${USER}/prob.py
COPY --chown=root:${USER} flag.txt /flag.txt

WORKDIR /home/${USER}

RUN chmod 550 ./start.sh &\
    chmod 440 ./prob.py &\
    chmod 440 /flag.txt &\
    chmod 440 /etc/xinetd.d/ctf

USER ${USER}

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf","-filelog","xinetd.log"]
