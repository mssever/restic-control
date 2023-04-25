#!/usr/bin/env python3
'''
This script wraps the restic command to enable scheduled backups. See the
README.md file for documentation.
'''

import os

from src import prerequisites

prerequisites.check_basic()

from subprocess import CalledProcessError

from src.boot import main, load_environment
from src.errors import handle_nonzero_exit

os.chdir(os.path.dirname(__file__))
load_environment()
if prerequisites.root_required() and os.geteuid() != 0:
    exit('This command with the current configuration must be run as root.')

try:
    exit(main())
except KeyboardInterrupt:
    exit(1)
except CalledProcessError as e:
    handle_nonzero_exit(e)
    exit(e.returncode)
