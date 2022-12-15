# docker build . --tag stack
# docker run --rm -d -p 6565:6565 -it stack

FROM ubuntu:18.04

# Install some libs
RUN apt-get update && apt-get -y upgrade && apt-get -y install python

# create ctf-user
RUN groupadd -r ctf && useradd -r -g ctf ctf

#add chall items
#ADD chall_init.sh /etc/chall_init.sh
COPY flag /home/ctf/flag-0bd94af70eb10471cff1ae9a2302322c.txt
COPY chall /home/ctf/
COPY launch.sh /home/ctf/
COPY ynetd /home/ctf/
# ADD redir.sh /home/ctf/redir.sh

#set some proper permissions
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/chall
RUN chmod 750 /home/ctf/ynetd
RUN chmod 750 /home/ctf/launch.sh
RUN chmod 440 /home/ctf/flag-0bd94af70eb10471cff1ae9a2302322c.txt


USER ctf
# COPY challenge.py .
EXPOSE 6565

CMD /home/ctf/ynetd -p 6565 /home/ctf/launch.sh

