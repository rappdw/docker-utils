import tempfile
from pathlib import Path
from dockerutils.gen_version import gen_version_file
from dockerutils.cd import cd
from dockerutils import __version__ as project_version
from dockerutils import pip_conf


def gen_version(test_dir, tmp_ver_file):
    test_env = Path(__file__).parent / test_dir
    with cd(test_env):
        gen_version_file(tmp_ver_file[1])
    with open(tmp_ver_file[1], 'r') as f:
        return f.read()

def test_versioneer():
    tmp_file = tempfile.mkstemp()
    version_contents = gen_version('sample-dir-versioneer', tmp_file)
    assert f'"version": "{project_version}"' in version_contents

def test_non_versioneer():
    tmp_file = tempfile.mkstemp()
    version_contents = gen_version('sample-dir', tmp_file)
    assert version_contents == ''

def test_pip_conf():
    test_env = Path(__file__).parent / 'sample-dir'
    with cd(test_env):
        pip_conf_file = test_env / 'pip.conf'
        assert not pip_conf_file.exists()
        with pip_conf(test_env):
            assert pip_conf_file.exists()
        assert not pip_conf_file.exists()
