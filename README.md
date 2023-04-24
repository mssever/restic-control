# restic-control

## What is this?

This is a thin wrapper around the [`restic`][restic] tool. It sets up the appropriate environment to enable me to easily run it as backup software.

## Installation

Before running this tool, you need to create a `.env` file in the project root directory, which contains the appropriate values to enable `restic` to run as intended. You can find an example to customize in `env_base.txt`. Running the tool without the `.env` file will cause `env_base.txt` to be copied to `.env`. This will help you get started, but you'll still have to edit `.env`.

Before running a backup, you should also create [includes][includes] and [excludes][excludes] files, as referenced in the sample `.env`.

## Usage

Except as indicated below, any arguments given to `restic_control.py` are passed unchanged to `restic`.

- If the first argument to `restic_control.py` is `backup`, then a backup will be triggered as configured from the `.env` file. All arguments except `backup` will be passed to `restic`. Note that `restic_control.py` will specify arguments of its own in addition to whatever is passed on the command line.
- If the first argument is `prune`, then this script will do `restic forget --prune` with the built in schedule of what to keep.
- A first argument of `check` runs a basic verification of the repository.
- A first argument of `check_read` does a `check`, followed by a test read of 1/7 of the repository, as determined by the day of the week.

### Combo commands

The following, when given as the first argument, run a combination of the above commands. The script only continues to the next command in the chain if the previous one exited with a status code of 0.

- `backup_check`: Runs `backup` followed by `check`.
- `backup_check_read`: Runs `backup` followed by `check_read`.

[excludes]: https://restic.readthedocs.io/en/stable/040_backup.html#excluding-files
[includes]: https://restic.readthedocs.io/en/stable/040_backup.html#including-files
[restic]: https://restic.readthedocs.io/
