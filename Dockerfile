FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openssh-server \
    openmpi-bin openmpi-common libopenmpi-dev \
    python3 python3-pip \
    iputils-ping net-tools \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir mpi4py numpy

RUN useradd -m -s /bin/bash mpiuser && mkdir -p /run/sshd

USER mpiuser
WORKDIR /home/mpiuser
RUN mkdir -p /home/mpiuser/.ssh && chmod 700 /home/mpiuser/.ssh \
 && ssh-keygen -t rsa -b 2048 -f /home/mpiuser/.ssh/id_rsa -N "" \
 && cp /home/mpiuser/.ssh/id_rsa.pub /home/mpiuser/.ssh/authorized_keys \
 && chmod 600 /home/mpiuser/.ssh/authorized_keys \
 && printf "Host *\n    StrictHostKeyChecking no\n    UserKnownHostsFile=/dev/null\n" > /home/mpiuser/.ssh/config \
 && chmod 600 /home/mpiuser/.ssh/config

COPY --chown=mpiuser:mpiuser hosts /home/mpiuser/hosts

USER root
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
