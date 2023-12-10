from . import on_ready
from . import test
from . import sync_commands
from . import archive

__all__ = [
    'on_ready',
    'test',
    'sync_commands',
    'archive',
]

def get_modules():
    return [on_ready, test, sync_commands, archive]
