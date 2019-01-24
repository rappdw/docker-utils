#!/usr/bin/env bash

# configure docker:
# put ubuntu user in docker group
# remove unix socket from docker config (we are going to allow TLS network sockets only)
# all key/cert setup is in register-dock script
sudo usermod -aG docker ubuntu
sudo systemctl stop docker
sudo sed -i 's"dockerd\ -H\ unix://"dockerd"g' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl start docker
