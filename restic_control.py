#!/usr/bin/env python3
'''
This script wraps the restic command to enable scheduled backups. See the
README.md file for documentation.
'''
try:
    import os
    from src.prerequisites import load_environment, check_basic, root_required

    os.chdir(os.path.dirname(__file__))
    load_environment()
    check_basic()

    from subprocess import CalledProcessError
    from src.boot import main
    from src.errors import handle_nonzero_exit

    if root_required() and os.geteuid() != 0:
        exit('This command with the current configuration must be run as root.')

    try:
        exit(main())
    except KeyboardInterrupt:
        exit(1)
    except CalledProcessError as e:
        handle_nonzero_exit(e)
        exit(e.returncode)
except Exception as e:
    from src.errors import report
    report(str(e))
    raise
