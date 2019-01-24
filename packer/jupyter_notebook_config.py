# from jupyter_core.paths import jupyter_data_dir
# import subprocess
import os
# import errno
# import stat
from subprocess import check_call

c = get_config()

c.NotebookApp.allow_origin = '*'
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.kernel_spec_manager_class = 'environment_kernels.EnvironmentKernelSpecManager'
c.EnvironmentKernelSpecManager.display_name_template="{}"
c.EnvironmentKernelSpecManager.conda_prefix_template="{}"
c.NotebookApp.iopub_data_rate_limit = 10000000000

session_params = ''
try:
    from credstash import get_session_params, listSecrets, getSecret
    session_params = get_session_params('ds-notebook', None)
    items = [item['name'] for item in listSecrets(**session_params) if item['name'] in [
        'notebook.password', 'notebook.token', 'github.client_id', 'github.client_secret', 'google.drive.client_id'
    ]]
except Exception:
    items = []

if 'notebook.password' in items:
    c.NotebookApp.password = "{secret}".format(secret=getSecret('notebook.password', **session_params))
if 'notebook.token' in items:
    c.NotebookApp.token = "{secret}".format(secret=getSecret('notebook.token', **session_params))
if 'github.client_id' in items:
    c.GitHubConfig.client_id = "{secret}".format(secret=getSecret('github.client_id', **session_params))
if 'github.client_secret' in items:
    c.GitHubConfig.client_secret = "{secret}".format(secret=getSecret('github.client_secret', **session_params))

# # Generate a self-signed certificate
# if 'GEN_CERT' in os.environ:
#     dir_name = jupyter_data_dir()
#     pem_file = os.path.join(dir_name, 'notebook.pem')
#     try:
#         os.makedirs(dir_name)
#     except OSError as exc:  # Python >2.5
#         if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
#             pass
#         else:
#             raise
#     # Generate a certificate if one doesn't exist on disk
#     subprocess.check_call(['openssl', 'req', '-new',
#                            '-newkey', 'rsa:2048',
#                            '-days', '365',
#                            '-nodes', '-x509',
#                            '-subj', '/C=XX/ST=XX/L=XX/O=generated/CN=generated',
#                            '-keyout', pem_file,
#                            '-out', pem_file])
#     # Restrict access to the file
#     os.chmod(pem_file, stat.S_IRUSR | stat.S_IWUSR)
#     c.NotebookApp.certfile = pem_file


# Autosave .html and .py versions of the notebook for easier diffing with version control systems
def post_save(model, os_path, contents_manager):
    """post-save hook for converting notebooks to .py scripts"""
    if model['type'] != 'notebook':
        return  # only do this for notebooks
    d, fname = os.path.split(os_path)
    output_dir = os.path.join(d, '.diffs')
    check_call(['jupyter', 'nbconvert', '--to', 'script', '--output-dir', output_dir, fname], cwd=d)
    check_call(['jupyter', 'nbconvert', '--to', 'html', '--output-dir', output_dir, fname], cwd=d)

if 'RESERO_JUPYTER_DIFFS' in os.environ and os.environ['RESERO_JUPYTER_DIFFS'] == '1':
    c.FileContentsManager.post_save_hook = post_save