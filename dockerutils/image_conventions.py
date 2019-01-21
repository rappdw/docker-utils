"""Functions that enforce conventions surrounding docker images."""
import sys
import logging
import os
import getpass
if sys.version_info < (3, 0):
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser

logger = logging.getLogger(__name__)


def get_root_dir():
    """
    get_root_dir will return the root directory of the project that contains a docker file.
     The constraints for our project with regard to docker are that there id a docker directoy as
     a top level sub-directory under the project root. The project root directory name is the base
     name of the docker file. There are sub-directories under docker that serve as the modes of
     various docker files that will be build (e.g. dev, lanista, jenkins, etc.)
    :return: root_directory for docker builda
    """
    docker_dir = os.path.join(os.getcwd(), 'docker')
    if os.path.exists(docker_dir) and os.path.isdir(docker_dir):
        return os.getcwd()
    else:
        raise ValueError('Unable to find docker directory. Invalid root: {dir}'.format(dir=os.getcwd()))


def get_default_project_name():
    return os.path.basename(get_root_dir()).lower()


def get_image_designation(image, config=None):
    if not config:
        os.path.join(get_root_dir(), os.path.join('docker', 'dockerutils.cfg'))
        config = ConfigParser()
        config.read(os.path.join(get_root_dir(), os.path.join('docker', 'dockerutils.cfg')))
    return get_image_name(config, image), get_image_tag(config, image)


def get_image_name(config, image):
    if image in config.sections():
        if 'name' in config.options(image):
            if 'prefix' not in config.options(image) or \
                    ('prefix' in config.options(image) and not config.get(image, 'prefix') in ['False', 'false', 'F', 'f']):
                return '{proj_name}-{image_name}'.format(
                    proj_name=get_default_project_name(),
                    image_name=config.get(image, "name")
                )
            else:
                return config.get(image, "name")
    return '{proj_name}-{image_name}'.format(
        proj_name=get_default_project_name(),
        image_name=image
    )


def get_image_tag(config, image):
    if image in config.sections():
        if 'tag' in config.options(image):
            return config.get(image, 'tag')
    return getpass.getuser()


def get_image_types(synthetic_images=None):
    docker_dir = os.path.join(get_root_dir(), 'docker')
    if synthetic_images is None:
        synthetic_images = []
    return [x for x in os.listdir(docker_dir) if os.path.isdir(os.path.join(docker_dir, x))] + synthetic_images
