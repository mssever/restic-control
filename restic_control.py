#!/usr/bin/env python3

import os
import shutil
import sys

from datetime import datetime
from subprocess import call, run

from dotenv import load_dotenv
import psutil

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

def make_prune_command():
    return [
        'forget',
        '--prune',
        '--keep-last', 1,
        '--keep-hourly', 2,
        '--keep-daily', 3,
        '--keep-weekly', 3,
        '--keep-monthly', 3,
        '--host', hostname(),
        '--cleanup-cache'
    ]

def make_check_command(read_data=None):
    cmd = ['check']
    if read_data:
        cmd += ['--read-data-subset', f'{read_data}/7']
    return cmd

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

def hostname():
    return run(['hostname'], capture_output=True, check=True, text=True).stdout.strip()

def repo_path():
    service = os.getenv('RESTIC_CONFIG_REMOTE_SERVICE')
    if service == 'wasabi':
        return f's3:https://{os.getenv("WASABI_SERVICE_URL")}/{os.getenv("WASABI_BUCKET_NAME")}'
    else:
        raise NotImplementedError(f'Unsupported remote service: {service}')

def load_environment():
    basedir = os.path.dirname(__file__)
    env_file = os.path.join(basedir, '.env')
    if not os.path.exists(env_file):
        print(f'Not configured yet. Please edit the file "{env_file}" and make the necessary configuration settings.')
        shutil.copyfile(os.path.join(basedir, 'env_base.txt'), env_file)
        exit(10)
    load_dotenv()

def exit_if_restic_already_running():
    if 'restic' in [i.name() for i in psutil.process_iter(['name'])]:
        # if 'restic' in proc:
            exit('A restic process is already running. Exiting.')

def parse_args():
    args = sys.argv
    switch = None
    if len(args) == 1:
        return (switch, [])
    elif args[1] == 'backup':
        switch = 'backup'
        del args[1]
    elif args[1] == 'prune':
        switch = 'prune'
        del args[1]
    return (switch, args[1:])

def main():
    exit_if_restic_already_running()
    switch, args = parse_args()
    load_environment()
    os.chdir(os.path.dirname(__file__))
    # if args.backup:
    #     return run_backup()
    if switch in ('backup', 'prune'):
        return call_restic(args, switch)
    elif switch is None:
        return call_restic(args)
    else:
        raise NotImplementedError()
    return 0

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        exit(1)
