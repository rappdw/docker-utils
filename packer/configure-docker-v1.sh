#!/usr/bin/env bash
sudo usermod -aG docker ubuntu
sudo systemctl stop docker
sudo sed -i 's"dockerd\ -H\ fd://"dockerd"g' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl start docker
