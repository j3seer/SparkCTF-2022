# docker build . --tag x-bof
# docker run --rm -d -p 6542:6542 -it f-xit
FROM ubuntu:20.04

EXPOSE 6542

RUN apt update && apt install -y socat
RUN useradd --user-group --system --no-log-init ctf

WORKDIR /home/ctf
COPY x-bof flag.txt run_challenge.sh ./
COPY glibc glibc
ENTRYPOINT ./run_challenge.sh

USER ctf
