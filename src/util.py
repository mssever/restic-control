import os
import subprocess

implemented_commands = ('backup', 'prune', 'check', 'check_read')

def hostname():
    return subprocess.run(['hostname'], capture_output=True, check=True, text=True).stdout.strip()

def repo_path():
    service = os.getenv('RESTIC_CONFIG_REMOTE_SERVICE')
    if service == 'wasabi':
        return f's3:https://{os.getenv("WASABI_SERVICE_URL")}/{os.getenv("WASABI_BUCKET_NAME")}'
    else:
        raise NotImplementedError(f'Unsupported remote service: {service}')
