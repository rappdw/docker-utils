# Use Cases and Design for 2.0

Opinionated, seamless, secure interaction with docker both local and remote.

## Execution Environments

* local virtual envrionment - can we autodetect this, e.g. look in ~/.venv and see if there is a <project> sub-directory
if os, automatically source ~/.venv/<project>/bin/activate

* local docker container - when should this be the preferred mode over local virtual envrionment? ENV setting? 
Something else?

* remote docker container - if DOCKER_HOST is set, target this execution environment. Any interaction with the remote
docker container should be wrapped by a sync-up and sync-down. Volume mounts assume code placed in 
/data/workspace/<user>/<project>. 

Opinions:
* local virtual environments are found under ~/.venv/<project>
* remote sync target found under /data/workspace/<user>/<project>
* Execution environment will be selected by some hint (ENV setting?)
* All commands and targets behave similarly regardless of execution ENV
* All required artifacts, AMIs, images, etc. will be publically available
* Configuration, proofpoint specific env, are not in code. preferably either cfg files (dockerutils.cfg) or credstash. 
Confgiruation is documented (in Configuration.md?)
* remote docker execution should be bracketed by sync-up/sync-down
* local docker execution should have "project" directory mounted into container

## Start a notebook

Need a script to setup a general notebook virtual environment analogous to docker-ds image. Perhaps
`setup-jupyter` - create a general virtual env for notebooks with standard python packages + jupyter extensions; 
pulls down docker-ds.

Navigate to any directory and start a notebook.

If there is a ~/.venv/<dir> virtual environment that supports jupyter, activate and use that env. 
If there isn't then use the general notebook virtual env or local/remote docker with docker-ds depending on execution
environment hint. If there is a setup.py or requirements.txt they should be installed into the selected virtual 
environment (Is this true for the general notebook virtual env?)

Opinions: 
* Notebooks are the pirmary env for data scientist
* `run-notebook` script to open notebook
* ideally, open browser to notebook (both local and remote)

## Command-line Interaction with code

Opinions:
* `run-shell` (activates execution enviornment, makes project available to execution environment, updates project with
modifications made in execution environment)
* command-line is a secondary env for data scientists


## Start remote server to host docker

Opinions:
* AMI is well-known
* ssh-key, security-group, etc. set at time of instance creation via configuration
* Accessed via source dock <ip> and castoff

## Questions

* Should we create sub-shells with env similar to pipenv?
* Should pipenv be used? if so how?
* What changes should be made to ~/.ssh/config to support this

## Other niceities
* Add monikers to /etc/hosts or ~/.ssh/config appropriately
