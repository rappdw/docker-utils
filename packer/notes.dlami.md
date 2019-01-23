# Notes on using the AWS DL AMI as the base image

We are using verison 20.0 (ami-0d0ff0945ae093aea) currently, but have modified it (by hand) to create our base image
The modifications are as follows:

1) ssh into image and wait for unattended upgrade to finish (time out) about 10 minutes
2) reboot
3) apt-get upgrade
4) reboot
5) apt-get remove docker-ce nvidia-docker2
6) run the "docker install" section of the setup.sh file
7) run the "docker configure" section of the setup.sh file (change "unix://" to "fd://")
8) apt-get upgrade
9) conda update -n base -c defaults conda
10) edit .profile, .dlamirc, .zshrc remove conda path and source /home/ubuntu/anaconda3/etc/profile.d/conda.sh in .profile
11) modify MOTD replace "source activate" with "conda activate" (/etc/update-motd.d/00-header)