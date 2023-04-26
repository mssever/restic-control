import os
import shutil
import sys

import psutil
from dotenv import load_dotenv

from . import call
from .util import implemented_commands

def exit_if_restic_already_running():
    if 'restic' in [i.name() for i in psutil.process_iter(['name'])]:
        exit('A restic process is already running. Exiting.')

def main():
    exit_if_restic_already_running()
    switch, args = parse_args()
    if switch in implemented_commands:
        return call.restic(args, switch)
    elif switch is not None and '/' in switch and all(s in implemented_commands for s in switch.split('/')):
        return call.combo(args, switch.split('/'))
    elif switch is None:
        return call.restic(args)
    else:
        raise NotImplementedError()

def parse_args():
    args = sys.argv[:]
    switch = None
    if len(args) == 1:
        return (switch, [])
    elif args[1] in implemented_commands or ('/' in args[1] and all(s in implemented_commands for s in args[1].split('/'))):
        switch = args[1]
        del args[1]
    return (switch, args[1:])
