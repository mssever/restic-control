import subprocess

from . import make
from .util import repo_path

def combo(args, calls):
    for call in calls:
        code = restic(args, call)
        if code != 0:
            return code
    return 0

def restic(args, mode=None):
    repo = ['-r', repo_path()]
    if mode == 'backup':
        main_cmd = make.backup_command()
    elif mode == 'prune':
        main_cmd = make.prune_command()
    elif mode == 'check':
        main_cmd = make.check_command()
    elif mode == 'check_read':
        main_cmd = make.check_command(datetime.now().weekday() + 1)
    else:
        main_cmd = []
    
    cmd = ['restic'] + main_cmd + repo + args
    code = subprocess.run([str(i) for i in cmd], check=True, text=True)
    if mode == 'backup' and code.returncode == 3:
        print('WARNING: Some files not backed up!')
    elif mode == 'backup' and code.returncode == 1:
        print('ERROR: Fatal error while backing up!')
    elif mode == 'prune' and code.returncode != 0:
        print('ERROR while pruning!')
    elif mode in ('check', 'check_read') and code.returncode != 0:
        print('ERROR: Check failed!')
    return code.returncode
