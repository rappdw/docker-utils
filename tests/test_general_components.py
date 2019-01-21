import os
import tempfile
from dockerutils.gen_version import gen_version_file
from dockerutils.cd import cd
from dockerutils import __version__ as project_version
from dockerutils import pip_conf


def gen_version(test_dir, tmp_ver_file):
    test_env = os.path.join(os.path.dirname(__file__), test_dir)
    with cd(test_env):
        gen_version_file(tmp_ver_file[1])
    with open(tmp_ver_file[1], 'r') as f:
        return f.read()

def test_versioneer():
    tmp_file = tempfile.mkstemp()
    version_contents = gen_version('sample-dir-versioneer', tmp_file)
    assert '"version": "{project_version}"'.format(project_version=project_version) in version_contents

def test_non_versioneer():
    tmp_file = tempfile.mkstemp()
    version_contents = gen_version('sample-dir', tmp_file)
    assert version_contents == ''

def test_pip_conf():
    test_env = os.path.join(os.path.dirname(__file__), 'sample-dir')
    with cd(test_env):
        pip_conf_file = os.path.join(test_env, 'pip.conf')
        assert not os.path.exists(pip_conf_file)
        with pip_conf(test_env):
            assert os.path.exists(pip_conf_file)
        assert not os.path.exists(pip_conf_file)
