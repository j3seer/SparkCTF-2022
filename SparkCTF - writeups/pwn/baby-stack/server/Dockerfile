# docker build . --tag baby-stack
# docker run --rm -d -p 1597:1597 -it baby-stack

FROM ubuntu:22.04

# Install some libs
RUN apt-get update && apt-get -y upgrade

# create ctf-user
RUN groupadd -r ctf && useradd -r -g ctf ctf

#add chall items
#ADD chall_init.sh /etc/chall_init.sh
COPY flag /home/ctf/flag-1858b78451951670fe41e56853f426ab.txt
COPY chall /home/ctf/
COPY launch.sh /home/ctf/
COPY ynetd /home/ctf/
# ADD redir.sh /home/ctf/redir.sh

#set some proper permissions
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/chall
RUN chmod 750 /home/ctf/ynetd
RUN chmod 750 /home/ctf/launch.sh
RUN chmod 440 /home/ctf/flag-1858b78451951670fe41e56853f426ab.txt


USER ctf
# COPY challenge.py .
EXPOSE 1597

CMD /home/ctf/ynetd -p 1597 /home/ctf/launch.sh
