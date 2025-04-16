FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    curl \
    supervisor

# Setup SSH
RUN mkdir /var/run/sshd && \
    echo "root:password" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Install Sensu agent
RUN curl -s https://packagecloud.io/install/repositories/sensu/stable/script.deb.sh | bash && \
    apt-get install -y sensu-go-agent

# Copy Sensu agent config and supervisor config
COPY agent.yml /etc/sensu/agent.yml
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose SSH port
EXPOSE 22

CMD ["/usr/bin/supervisord", "-n"]