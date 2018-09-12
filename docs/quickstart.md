# docker-utils Quick Start

## Install
```bash
$ pip3 install -U dockerutils

# Show installed version and latest version
$ pip3 search dockerutils

# If you are unable to install the latest version, try:
$ pip3 install -U --force-reinstall dockerutils==<latest version>

# Show help
$ create-dock -h

# Create remote dock instance using defaults. You will be prompted before creation.
$ create-dock
```


## Additional Commands
```bash

# Connect to remote secure docker
$ source dock <ip|moniker>

# Sync local files to remote instance
$ sync-up

# Sync remote changes to local worksation
$ sync-down

# After 'source dock <ip|moniker>'
$ bin/notebook
$ bin/dev

# Disconnect from remote secure docker
$ castoff

```
