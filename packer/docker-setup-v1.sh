#!/usr/bin/env bash
## Here we are installing docker, just to test
# sudo curl -fsSL get.docker.com -o /tmp/get-docker.sh
# sudo sh /tmp/get-docker.sh
sudo usermod -aG docker ubuntu
sudo systemctl stop docker
sudo sed -i 's"dockerd\ -H\ fd://"dockerd"g' /etc/systemd/system/multi-user.target.wants/docker.service
sudo sed -i 's"dockerd\ -H\ fd://"dockerd"g' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl start docker
