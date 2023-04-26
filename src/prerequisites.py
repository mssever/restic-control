import os
import shutil
import sys
import warnings


try:
    from dotenv import load_dotenv
except ImportError:
    exit('The dotenv module is required.\n\nsudo apt install python3-dotenv')

try:
    import psutil
except ImportError:
    exit('The psutil module is required.\n\nsudo apt install python3-psutil')

class PrerequisiteError(Exception):
    pass

def check_basic():
    if shutil.which('restic') is None:
        raise PrerequisiteError('The restic command is not available on this system!')

def load_environment():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = os.path.join(basedir, '.env')
    if not os.path.exists(env_file):
        print(f'Not configured yet. Please edit the file "{env_file}" and make the necessary configuration settings.')
        shutil.copyfile(os.path.join(basedir, 'env_base.txt'), env_file)
        exit(10)
    load_dotenv()

def root_required():
    if len(sys.argv) > 1 and 'backup' in sys.argv[1]:
        try:
            with open(os.environ['RESTIC_INCLUDES_FILE']) as f:
                for line in f.readlines():
                    if _directory_requires_root(line.strip()):
                        return True
        except KeyError:
            return False

def _directory_requires_root(dir):
    if not os.path.isdir(dir):
        return False
    dir = os.path.abspath(dir)
    max_depth = 3
    for root, dirs, files in os.walk(dir):
        if root[len(dir):].count(os.sep) < max_depth:
            for f in files:
                the_file = os.path.join(root, f)
                if not os.access(the_file, os.R_OK):
                    return True
        else:
            break
    return False
