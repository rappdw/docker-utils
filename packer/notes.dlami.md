# How to Build/Deploy a Resero-labs dlami

We are using verison 22.0 (ami-01a4e5be5f289dd12) currently, but have modified it (by hand) to create our base image

1) create instance of DLAMI. (Watch for updates [Deep Learning AMI (Ubuntu)](https://aws.amazon.com/marketplace/pp/B077GCH38C).) 

    `create-dock -a ami-01a4e5be5f289dd12 -s -m base-ami -i p3.2xlarge`
2) ssh into image.
 
    `ssh-dock base-ami`
3) Wait for /var/log/unattended-upgrades/unattended-upgrades.log to emit a line. 
that looks like: `2019-01-24 17:52:10,320 INFO All upgrades installed` (should be aobut 15 minutes)

4) reboot

    ```bash
    stop-dock base-ami
    start-dock base-ami
    ```
5) run upgrade.sh script

    ```bash
    scp upgrade.sh <base-ami-ip>:~/
    ssh-dock base-ami
    ./upgrade.sh
    ```
6) reboot and ensure that nvidia drivers still good

    `nvidia-smi`
7) Create an image from this instance

    `aws ec2 create-image --instance-id i-0238495638422d858 --name resero-labs-dlami-base-22.0-2019.04`

    (Instance id can be found in the console or in  `~/.docker/<ip-addr>/connection_config.txt`. 
    AMI name should follow the convention `resero-labs-dlami-base-<dlami-version>-<date-created>`)
8) Terminate the base-ami dock

    `destroy-dock base-ami -f`
9) Use the ami from previous step as the base ami in the packer script

    ```bash
    edit resero-labs-dl.packer and update both the "name" and "source_ami" values appropriately
    packer build resero-labs-dl.packer
    ```

10) Validate the new ami

    ```bash
    create-dock -a <resero-labs-dlami-candidate> -m test-ami -i p3.2xlarge
    source dock test-ami
    docker images
    ssh-dock
    nvidia-smi
    castoff
    destroy-dock test-ami -f
    ```

11) Switch names of previous resero-labs-dlami with the one just created

