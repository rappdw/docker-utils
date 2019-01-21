import os
from dockerutils.cd import cd
from dockerutils.image_conventions import get_image_designation, get_image_types

def test_image_designation():
    test_project = os.path.join(os.path.dirname(__file__), 'sample-dir')
    with cd(test_project):
        designation = get_image_designation('test')
        assert designation == ('sample-dir-test', 'latest')

def test_image_types():
    test_project = os.path.join(os.path.dirname(__file__), 'sample-dir')
    with cd(test_project):
        assert get_image_types() == ['test']
        assert get_image_types(['a', 'b']) == ['test', 'a', 'b']
