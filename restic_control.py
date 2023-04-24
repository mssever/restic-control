#!/usr/bin/env python3

import os
import shutil
import sys

from datetime import datetime
from subprocess import call, run

from dotenv import load_dotenv
import psutil

implemented_commands = ('backup', 'prune', 'check', 'check_read')
#implemented_combo_commands = ('backup_check', 'backup_check_read')

def call_combo(args, calls):
    for call in calls:
        code = call_restic(args, call)
        if code != 0:
            return code
    return 0

def call_restic(args, mode=None):
    repo = ['-r', repo_path()]
    if mode == 'backup':
        main_cmd = make_backup_command()
    elif mode == 'prune':
        main_cmd = make_prune_command()
    elif mode == 'check':
        main_cmd = make_check_command()
    elif mode == 'check_read':
        main_cmd = make_check_command(datetime.now().weekday() + 1)
    else:
        main_cmd = []
    
    cmd = ['restic'] + main_cmd + repo + args
    code = call(str(i) for i in cmd)
    if mode == 'backup' and code == 3:
        print('WARNING: Some files not backed up!')
    elif mode == 'backup' and code == 1:
        print('ERROR: Fatal error while backing up!')
    elif mode == 'prune' and code != 0:
        print('ERROR while pruning!')
    elif mode in ('check', 'check_read') and code != 0:
        print('ERROR: Check failed!')
    return code

def exit_if_restic_already_running():
    if 'restic' in [i.name() for i in psutil.process_iter(['name'])]:
        exit('A restic process is already running. Exiting.')

def hostname():
    return run(['hostname'], capture_output=True, check=True, text=True).stdout.strip()

def load_environment():
    basedir = os.path.dirname(__file__)
    env_file = os.path.join(basedir, '.env')
    if not os.path.exists(env_file):
        print(f'Not configured yet. Please edit the file "{env_file}" and make the necessary configuration settings.')
        shutil.copyfile(os.path.join(basedir, 'env_base.txt'), env_file)
        exit(10)
    load_dotenv()

def main():
    exit_if_restic_already_running()
    os.chdir(os.path.dirname(__file__))
    switch, args = parse_args()
    load_environment()
    if switch in implemented_commands:
        return call_restic(args, switch)
    elif switch is not None and '/' in switch and all(s in implemented_commands for s in switch.split('/')):
        return call_combo(args, switch.split('/'))
    elif switch is None:
        return call_restic(args)
    else:
        raise NotImplementedError()

def make_backup_command():
    try:
        include = ['--files-from', os.environ['RESTIC_INCLUDES_FILE']]
        if not os.path.isfile(include[1]):
            raise FileNotFoundError('Includes file configured but not found')
    except KeyError:
        include = []
    try:
        exclude = ['--exclude-file', os.environ['RESTIC_EXCLUDES_FILE']]
        if not os.path.isfile(exclude[1]):
            raise FileNotFoundError('Excludes file configured but not found')
    except KeyError:
        exclude = []
    return ['backup'] + include + exclude

def make_check_command(read_data=None):
    cmd = ['check']
    if read_data:
        cmd += ['--read-data-subset', f'{read_data}/7']
    return cmd

def make_prune_command():
    return [
        'forget',
        '--prune',
        '--keep-last', os.environ['RESTIC_PRUNE_KEEP_LAST'],
        '--keep-hourly', os.environ['RESTIC_PRUNE_KEEP_HOURLY'],
        '--keep-daily', os.environ['RESTIC_PRUNE_KEEP_DAILY'],
        '--keep-weekly', os.environ['RESTIC_PRUNE_KEEP_WEEKLY'],
        '--keep-monthly', os.environ['RESTIC_PRUNE_KEEP_MONTHLY'],
        '--host', hostname(),
        '--cleanup-cache'
    ]

def parse_args():
    args = sys.argv
    switch = None
    if len(args) == 1:
        return (switch, [])
    elif args[1] in implemented_commands or ('/' in args[1] and all(s in implemented_commands for s in args[1].split('/'))):
        switch = args[1]
        del args[1]
    return (switch, args[1:])

def repo_path():
    service = os.getenv('RESTIC_CONFIG_REMOTE_SERVICE')
    if service == 'wasabi':
        return f's3:https://{os.getenv("WASABI_SERVICE_URL")}/{os.getenv("WASABI_BUCKET_NAME")}'
    else:
        raise NotImplementedError(f'Unsupported remote service: {service}')

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        exit(1)
