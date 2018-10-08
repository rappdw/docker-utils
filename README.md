[![TravisCI](https://api.travis-ci.org/resero-labs/docker-utils.svg?branch=master)](https://travis-ci.org/resero-labs/docker-utils) [![Coverage](https://codecov.io/gh/resero-labs/docker-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/resero-labs/docker-utils) [![PyPi](https://img.shields.io/pypi/v/dockerutils.svg)](https://pypi.org/project/dockerutils/) [![PyPi](https://img.shields.io/pypi/wheel/dockerutils.svg)](https://pypi.org/project/dockerutils/) [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) 

# Docker Utilities/Patterns for Python Projects

`dockerutils` defines a set of patterns and utilities to facilitate use of docker with a python app or library 
facilitating:
* seperating development/test dependencies out of production container, e.g. production container vs. dev/test container
* seperating data science notebook container from execution container
* environment experimentation
* cases in which you want to "freeze" any external dependencies in one container and use that as a base
for containers that are dependent solely on the project

## Conventions

1) Create a docker directory tree at the root of the project

    In this directory tree there should be one sub-directory for each unique docker container type that is desired.
    Each of these sub-directories would contain the `Dockerfile` that will be used to create the image
    as well as any source specific to that image.
2) Use versioneer for project versioning. 

    As part of the image build, a file, `_version.py.bld`, will be generated and placed at the project 
    root. A `Dockerfile` can add that file to the image on creation to prevent the need for including the
    .git directory tree in the container context (usually quite expensive).
3) Create a docker/base directory to make use of built in external dependency isolation

    This capability supports environments where a docker build isn't able to access external dependencies (Docker Hub, 
    pypi, etc.), for instance a server in a "locked-down" environment. A base image can be defined to isolate any 
    dependencies that are required. That image can then be built and `transfer-image` used to transfer the base image 
    to the target environment.
     
    Subsequent images can be built based off of that image that are "self-contained" (relying only on source
    from the project). The remote docker api can then be used to quickly iterate only requiring the more
    cumbersome transfer-image to be used when external dependencies change.
4) Building and running images controlled through configuration (<project_dir>/docker/dockerutils.cfg)

    Includes setting most docker parameters, i.e. volume mounts, ports, networks, commands, etc. with
    replacement varilable support for things like user, project root, etc.
    
## Command-line Interface

`build-image` takes the name of one of the sub-directories in the `docker` directory and builds the
image defined therein. The image is named \<project\>-\<subdir\>:\<user\>

`run-image` takes the name of one of the sub-directories (or one of the synthetic images defined in `dockerutils.cfg`), 
together with any of the configuration for that image defined in `dockerutils.cfg` and starts a docker container

`transfer-image` takes a docker image name and uses docker `save` and `load` to transfer the image to a remote host

`publish-image` takes the name of one of the sub-directories in the `docker` directory and pushes the image built by 
the docker file to the defined repository (AWS or Docker)

`run-notebook` will start a docker container using either the notebook container found in the `docker/notebook` directory
if it exists, or [rappdw/docker-ds](https://github.com/rappdw/docker-ds) otherwise. The current directory will be mounted
into the container for use in the Juypter notebook environment. There are a couple of environment variable to be aware of 
with this command:

* DOCKER_DS_DONT_PULL - if set, the version of rappdw/docker-ds currently available will be used rather than pulling 
the latest version from docker hub.
* DOCKER_DS_DIFFS - if set,  

## `dockerutils.cfg` Format
Configuration in `docker/dockerutils.cfg` is used to configure behavior of the `dockerutils` scripts.

### Image Section
The `dockerutils.cfg` file format allows for configuration sections named corresponding to the sub-directories in the 
docker directory tree. Each of these sections may contain one of the following:

* `environment` - in the form of (`-e VAR=value`)+ to pass environment into the container
* `interactive` - either -e or -it
*  `gpu` - conforms to NVIDIA Docker 2.0 specification, e.g. `--runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all`, 
`run-image -g` will add this automatically
* `network` - the name of the network for the container
* `volumes` - in the form of (`-v <host-dir>:<container-dir>`)+ or (`--mount ...`)+ or both
* `ports` - in the form of (`-p <host-port>:<container-port>`)+
* `cmd` - any valid Docker `CMD` specification
* `pull_FROM_on_force` - defaults to False, if True, add --pull to build command when force building image (or base image)
* `image_repo` - the repository to publish the image to
* `publication_tag` - the tag for publication (full image name + tag) 
* `pre_build_script` - A shell command or script to run before a docker build is issued
* `post_build_script` - A shell command or script to run after a docker build has been compeleted (successfully)

### Synthetic Images
Additionally, "synthetic" images can be specified by adding a `run-image` section with a `synthetic_images` definition
that contains a list of "synthetic" images. Each of these may also have a named section as defined for the docker
sub-directories, but must also contain a `name` value that resolves to one of the docker sub-directories. For example:

```
[run_image]
synthetic_images=shell

[shell]
name=dev
...
```

### Image Tagging
The default tag for any image created/run/etc. is the user name in the host environment when running the 
utility. This can be overriden by adding a `tag` value to the desired section. For example:

```
[dev]
tag=experiment.2017.12.16
...
```
### Volume Replacement Variables

The volume specification may contain either environment variables (`$name` and `${name}` formats) as well as specific
variable replacement designations of the form `{var}`.  The supported variables include:

* `project_root` - will be replaced with the root directory name of the project
* `user` - will be replaced with the user name of the user running the command
* `project` - replace with project namge

### Image Push Replacement Variables

* `account` - AWS account designation
* `region` - AWS region
* `image` - Image name
* `tag` - Image tag 
* `user` - will be replaced with the user name of the user running the command

### Publish to AWS
In order to publish to AWS, the repository will be the image name and the following should
be configured for images that are published to AWS

```
image_repo=aws
publication_tag={account}.dkr.ecr.{region}.amazonaws.com/{image}:{tag}"
```

## Patterns

### Running your code in container, making live modifications outside container in your editor of choice     

If you're like me, you have a whole set of tools in your host environment that you use to work with your project.
One of the disadvantages of working with Docker can be the difficulty of transplanting those tools into the container
environment. Perhaps there is a way to have your cake and eat it too!
The `dev` example does a reasonable job of doing just this. 

With this pattern, you create a `Dockerfile` that has everything in the image *except* for your project source. An
empty `WORKDIR` is created and then `ENTRYPOINT` even does a `pip install -e` of the contents of the empty `WORKDIR`. 
We get the desired results by mounting the source project directory into the container's `WORKDIR` (see `dev` section
of `docker/dockertuils.cfg`).

With this pattern you can run tests, experiment, etc. in container, make changes to the project in your host 
environment toolset and immediately observe the changes that were made.
   
### Working with a server in a locked-down environment
You may find yourself in a situation in which you need to work with a server hosting Docker in an environment that has
limited access to the "outside world". This pattern can be used to capture all external dependencies in a base 
image that is built in an environment that is open, use `transfer-image` to send this base image to the server and
then utilize a derived image dependent just on project sources and the base image to iterate without requiring open
access on the server.
 
### Adding test frameworks, code analysis tools, etc. to a container for testing/validation

### Tensorflow for both CPU and GPU in the same container
It is sometimes useful to try both the CPU and GPU versions of Tensorflow. The example in `docker/tensorflow` provides
a pattern to do so. All tensorflow depdendencies are installed into global python site-packages. Then virtual 
environments are created for both cpu and gpu versions and the appropriate version of tensorflow is install into 
the respective virtual environments.

The `run-image` script makes use of NVIDIA Docker 2.0 being installed on the host os. When run with the `-g` option,
the NVIDIA runtime will be used to make GPUs available in container.

Upon container startup, the appropriate virtual environment (cpu or gpu) will be activated dependant upon the 
`-g` option.

To switch between virtual envrionments utilized the symbolic links, `/cpu-env` and `/gpu-env`, e.g. 
`source /cpu-env`.

### Versioneer support
If you aren't using [versioneer](https://github.com/warner/python-versioneer) to version your Python projects, you 
should be. Versioneer utilizes .git to determine the project version. Having correct version information in container 
is desireable in many cases, but pushing .git into container usually isn't desireable. To capture version information
for container, the `genversion` utility is available and uses capabilities of versioneer to generate a _version.py.bld
file in the project root. This file is available for `Dockerfile` to add/overwrite the version.py file within the 
Docker image. An example of this is found in the cicd sub-directory.

### `.dockerignore`
In order to minimize the context sent to Docker to build images, please see examples in `.dockerignore` in this
repository.

## A Note on Implementation
We selected to use the Docker command line from python scripts rather than the [Docker
API available to Python](https://pypi.python.org/pypi/docker/) as it integrates better into my development loop. As each CLI prints 
the Docker command it's using, if it does something unexpected, it's each to copy and paste
the command used, modify it and be on your way without having to debug through CLI utility code, 
allowing bugs/additions to the CLI to be addressed at a later point outside the context of a
project development loop.
