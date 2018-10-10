
[systemctl](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)

It looks like docker is already registered as a service that will auto restart

```
ubuntu@ip-10-93-135-30:~$ sudo systemctl enable docker
Synchronizing state of docker.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable docker
Failed to enable unit: File /etc/systemd/system/multi-user.target.wants/docker.service already exists.
```

Need to look at what exactly stop/start does

According to [AWS Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html), the instance
performs a normal shutdown.

Steps to Diagnose

1) create-dock -m test
2) ssh-dock test
3) verify docker is running
4) `date >timestamp.log`
5) `sudo journalctl -u docker.service >docker.log`
6) exit
7) stop-dock test
8) start-dock test
9) ssh-dock test
10) verify docker is not running
11) `date >timestamp.restart.log`
12) `sudo journalctl -u docker.service >docker.reboot.log`


# On Jeremy's system
``` 
root@ip-10-93-135-93:/home/ubuntu# systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
     Docs: https://docs.docker.com


```
from journalctl -u docker
``` 
Oct 10 13:23:35 ip-10-93-135-93 systemd[1]: Started Docker Application Container Engine.
Oct 10 13:23:36 ip-10-93-135-93 dockerd[16334]: http: TLS handshake error from 10.92.8.39:52312: remote error: tls: bad certificate
Oct 10 13:23:36 ip-10-93-135-93 dockerd[16334]: http: TLS handshake error from 10.92.8.39:52313: remote error: tls: bad certificate
Oct 10 13:35:11 ip-10-93-135-93 systemd[1]: Stopping Docker Application Container Engine...
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.152596710Z" level=info msg="Processing signal 'terminated'"
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.154355239Z" level=info msg="stopping event stream following graceful shutdown" error="
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.154381095Z" level=info msg="stopping healthcheck following graceful shutdown" module=l
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.154438958Z" level=info msg="stopping event stream following graceful shutdown" error="
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.154853556Z" level=info msg="pickfirstBalancer: HandleSubConnStateChange: 0xc4204532c0,
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.154876801Z" level=info msg="pickfirstBalancer: HandleSubConnStateChange: 0xc4204532c0,
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.155033817Z" level=info msg="pickfirstBalancer: HandleSubConnStateChange: 0xc42003a330,
Oct 10 13:35:11 ip-10-93-135-93 dockerd[16334]: time="2018-10-10T13:35:11.155051869Z" level=info msg="pickfirstBalancer: HandleSubConnStateChange: 0xc42003a330,
Oct 10 13:35:12 ip-10-93-135-93 systemd[1]: Stopped Docker Application Container Engine.
```
Current time is: Wed Oct 10 13:45:33 UTC 2018

## Resolution

The problem was in the `packer/configure-docker-v1.sh` script which had the line:

``` 
sudo sed -i 's"dockerd\ -H\ fd://"dockerd"g' /etc/systemd/system/multi-user.target.wants/docker.service
```

`/etc/systemd/system/multi-user.target.wants/docker.service` is a symlink to `/lib/systemd/system/docker.service`. 
Running sed against it, turned it into a file. This caused the service to not be recognized as enabled
by `systemd`.