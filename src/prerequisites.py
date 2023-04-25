import os
import shutil
import sys
import warnings

from . import errors

try:
    from dotenv import load_dotenv
except ImportError:
    exit('The dotenv module is required.\n\nsudo apt install python3-dotenv')

try:
    import psutil
except ImportError:
    exit('The psutil module is required.\n\nsudo apt install python3-psutil')

def check_basic():
    failed = []
    for prereq in ('restic', 'yad', 'notify-send'):
        if shutil.which(prereq) is None:
            failed.append(prereq)
    if len(failed) != 0:
        if 'restic' in failed:
            raise errors.PrerequisiteError('The restic command is not available on this system!')
        else:
            [warnings.warn(f'The command "{i}" is not available, so its features will not work!') for i in failed]

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
