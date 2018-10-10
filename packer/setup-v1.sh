#!/usr/bin/env bash

# wait just a bit to allow everything to settle down
sleep 30

# update apt and install dependencies
sudo apt-get update
sudo apt-get install -y gcc make apt-transport-https ca-certificates curl software-properties-common

# get the latest nvidia drivers and install them
wget -P /tmp http://us.download.nvidia.com/tesla/396.44/NVIDIA-Linux-x86_64-396.44.run
chmod +x /tmp/NVIDIA-Linux-x86_64-396.44.run
sudo /tmp/NVIDIA-Linux-x86_64-396.44.run -silent

# now get docker and nvidia-docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable'
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y docker-ce=18.06.0~ce~3-0~ubuntu
sudo apt-get install -y nvidia-docker2
