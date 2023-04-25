class PrerequisiteError(Exception):
    pass

def handle_nonzero_exit(exc):
    msg = f'A restic job exited with code {exc.returncode}. Please investigate.\n\nCommand:\n\t{exc.cmd}\nCalled by:\n\t{" ".join(sys.argv)}\nOutput:\n\t{exc.output}\nstderr:\n\t{exc.stderr}\nstdout:\n\t{exc.stdout}'
    call(['notify-send', '--urgency', 'critical', '--icon', 'warning', msg])
    call(['yad', '--text-info', '--title', 'Restic Backup Error', '--window-icon', 'warning', '--image', 'warning', '--text', msg, '--button', 'gtk-close', '--sticky', '--on-top'])
