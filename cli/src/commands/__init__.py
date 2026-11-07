"""Command handlers for the Dev-Team CLI."""

from .doctor import doctor_command
from .init import init_command
from .install import install_command
from .list import list_command
from .status import status_command
from .uninstall import uninstall_command
from .update import update_command

__all__ = [
    "doctor_command",
    "init_command",
    "install_command",
    "list_command",
    "status_command",
    "uninstall_command",
    "update_command",
]

