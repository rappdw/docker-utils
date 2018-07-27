"""Functions that enforce conventions surrounding docker images."""
import configparser
import logging
import os
import getpass
import sys

logger = logging.getLogger(__name__)


_ROOT_DIR = None
def get_root_dir():
    '''
    get_root_dir will return the root directory of the project that contains a docker file.
     The constraints for our project with regard to docker are that there id a docker directoy as
     a top level sub-directory under the project root. The project root directory name is the base
     name of the docker file. There are sub-directories under docker that serve as the modes of
     various docker files that will be build (e.g. dev, lanista, jenkins, etc.)
    :return: root_directory for docker builda
    '''
    global _ROOT_DIR # pylint: disable=global-statement

    if _ROOT_DIR is None:
        docker_dir = os.path.join(os.getcwd(), 'docker')
        if os.path.exists(docker_dir) and os.path.isdir(docker_dir):
            _ROOT_DIR = os.getcwd()
        else:
            raise ValueError(f'Unable to find docker directory. Invalid root: {os.getcwd()}')

    return _ROOT_DIR


def get_default_project_name():
    return os.path.basename(get_root_dir()).lower()


def get_image_designation(image, config=None):
    if not config:
        os.path.join(get_root_dir(), os.path.join('docker', 'dockerutils.cfg'))
        config = configparser.ConfigParser()
        config.read(os.path.join(get_root_dir(), os.path.join('docker', 'dockerutils.cfg')))
    return (get_image_name(config, image), get_image_tag(config, image))


def get_image_name(config, image):
    if image in config.sections():
        if 'name' in config[image]:
            return f'{get_default_project_name()}-{config[image]["name"]}'
    return f'{get_default_project_name()}-{image}'


def get_image_tag(config, image):
    if image in config.sections():
        if 'tag' in config[image]:
            return config[image]['tag']
    return getpass.getuser()


def get_image_types(synthetic_images=None):
    docker_dir = os.path.join(get_root_dir(), 'docker')
    if synthetic_images is None:
        synthetic_images = []
    return [x for x in os.listdir(docker_dir) if os.path.isdir(os.path.join(docker_dir, x))] + synthetic_images
