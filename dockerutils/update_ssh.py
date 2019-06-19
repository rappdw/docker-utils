from os.path import expanduser
from .sshconf import read_ssh_config

def add_dock(host, ip, user):
    cfg = read_ssh_config(expanduser("~/.ssh/config"))
    # in the future, we could add things like ProxyJump, etc. here...
    cfg.add(host, Hostname=ip, User=user, UserKnownHostsFile="/dev/null", StrictHostKeyChecking="no", ServerAliveInterval="60", LogLevel="ERROR")
    cfg.write(expanduser("~/.ssh/config"))


def remove_dock(host):
    cfg = read_ssh_config(expanduser("~/.ssh/config"))
    cfg.remove(host)
    cfg.write(expanduser("~/.ssh/config"))
