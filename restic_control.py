#!/usr/bin/env python3

# import argparse
import os
import shutil
import sys

from datetime import datetime
from dotenv import load_dotenv
from subprocess import call

import psutil

# def run_backup():
#     cmd = [
#         'restic',
#         '-r',
#         repo_path(),
#         'backup',
#         '/home/scott'
#     ]
#     return call(cmd)
def call_restic(args, mode=None):
    repo = ['-r', repo_path()]
    other = []
    if mode == 'backup':
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
        other = ['backup'] + other + include + exclude
        dt = datetime.now()
        other += ['--tag',
                  f'date={dt.date().strftime("%Y-%m-%d")}',
                  '--tag',
                  f'time={dt.time().strftime("%H:%M:%S")}'
                 ]
    
    cmd = ['restic'] + repo + other + args
    return call(cmd)

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
    return (switch, args[1:])

def main():
    exit_if_restic_already_running()
    switch, args = parse_args()
    load_environment()
    os.chdir(os.path.dirname(__file__))
    # if args.backup:
    #     return run_backup()
    if switch == 'backup':
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
