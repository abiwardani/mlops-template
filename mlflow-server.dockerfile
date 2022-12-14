FROM python:3.7.13

# Env & Arg variables
ARG USERNAME=pythonssh
ARG USERPASS=sshpass

# Apt update & apt install required packages
# whois: required for mkpasswd
RUN apt update && apt -y install openssh-server whois

# Add a non-root user & set password
RUN useradd -ms /bin/bash $USERNAME
# Save username on a file ¿?¿?¿?¿?¿?
#RUN echo "$USERNAME" > /.non-root-username

# Set password for non-root user
RUN usermod --password $(echo "$USERPASS" | mkpasswd -s) $USERNAME

# Remove no-needed packages
RUN apt purge -y whois && apt -y autoremove && apt -y autoclean && apt -y clean

# Change to non-root user
#USER $USERNAME
#WORKDIR /home/$USERNAME

# Copy the entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set permissions /etc/ssh
RUN chmod -r 600 /etc/ssh

# Copy the sshd config file
COPY sshd_config /etc/ssh/sshd_config
RUN chmod +x /etc/ssh/sshd_config

# Create the ssh directory and authorized_keys file
USER $USERNAME
RUN mkdir /home/$USERNAME/.ssh && touch /home/$USERNAME/.ssh/authorized_keys
USER root

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && apt-get install lsof \
    && mkdir -p /opt/airflow/mlruns
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

# Expose SSH port
EXPOSE 22

# Set volumes
VOLUME /home/$USERNAME/.ssh
VOLUME /etc/ssh

# Run entrypoint
CMD ["/entrypoint.sh"]
