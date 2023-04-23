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

[excludes]: https://restic.readthedocs.io/en/stable/040_backup.html#excluding-files
[includes]: https://restic.readthedocs.io/en/stable/040_backup.html#including-files
[restic]: https://restic.readthedocs.io/
