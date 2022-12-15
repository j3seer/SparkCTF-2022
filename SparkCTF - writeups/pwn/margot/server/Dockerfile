FROM ubuntu:20.04

EXPOSE 7894

RUN apt update && apt install -y socat
RUN useradd --user-group --system --no-log-init ctf

WORKDIR /home/ctf
COPY margot flag.txt run_challenge.sh ./
COPY glibc glibc
ENTRYPOINT ./run_challenge.sh

USER ctf
