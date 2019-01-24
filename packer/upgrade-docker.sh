#!/usr/bin/env bash

# install dependencies
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2
    software-properties-common

# remove docker and nvidia-docker2 so we can reinstall them from appropriate source
sudo apt-get remove -y \
    docker-ce \
    nvidia-docker2

# now get docker and nvidia-docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y \
    docker-ce \
    nvidia-docker2

