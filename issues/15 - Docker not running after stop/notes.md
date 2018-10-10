
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