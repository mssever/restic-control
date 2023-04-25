import os
from .util import hostname

def backup_command():
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

def check_command(read_data=None):
    cmd = ['check']
    if read_data:
        cmd += ['--read-data-subset', f'{read_data}/7']
    return cmd

def prune_command():
    return [
        'forget',
        '--prune',
        '--keep-last', os.environ.get('RESTIC_PRUNE_KEEP_LAST', 5),
        '--keep-hourly', os.environ.get('RESTIC_PRUNE_KEEP_HOURLY', 24),
        '--keep-daily', os.environ.get('RESTIC_PRUNE_KEEP_DAILY', 7),
        '--keep-weekly', os.environ.get('RESTIC_PRUNE_KEEP_WEEKLY', 4),
        '--keep-monthly', os.environ.get('RESTIC_PRUNE_KEEP_MONTHLY', 12),
        '--host', hostname(),
        '--cleanup-cache'
    ]
