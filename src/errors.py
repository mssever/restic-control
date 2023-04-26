import os
import shutil
import sys
from subprocess import call
from warnings import warn

error_reporting = os.environ.get('RESTIC_CONTROL_ERROR_REPORTING', 'print')
if error_reporting not in ('print', 'notify', 'nc'):
    error_reporting = 'print'

def report(msg):
    if error_reporting == 'print':
        sys.stderr.write(msg.rstrip() + '\n')
    elif error_reporting == 'notify':
        call(['notify-send', '--urgency', 'critical',
              '--icon', 'warning', msg])
        call(['yad', '--text-info', '--title', 'Restic Backup Error',
              '--window-icon', 'warning', '--image', 'warning', '--text', msg,
              '--button', 'gtk-close', '--sticky', '--on-top'])
    elif error_reporting == 'nc':
        raise NotImplementedError
    else:
        raise NotImplementedError

def handle_nonzero_exit(exc):
    msg = f'A restic job exited with code {exc.returncode}. Please investigate.\n\nCommand:\n\t{exc.cmd}\nCalled by:\n\t{" ".join(sys.argv)}\nOutput:\n\t{exc.output}\nstderr:\n\t{exc.stderr}\nstdout:\n\t{exc.stdout}'
    report(msg)

def _check_error_prereqs():
    if error_reporting == 'notify':
        failed = []
        for prereq in ('yad', 'notify-send'):
            if shutil.which(prereq) is None:
                failed.append(prereq)
        if len(failed) != 0:
            msg = 'The command "{}" is not available, so its features will not work!'
            for i in failed:
                warn(msg.format(i))
            exit(1)
    if error_reporting == 'nc' and shutil.which('nc') is None:
        exit("ERROR: Can't use the nc command to report errors because it isn't installed.")

_check_error_prereqs()
