"""Installation and asset distribution module for Dev-Team."""

from .global_installer import GlobalInstallResult, install_global
from .strategies import copy_directory_contents, copy_file_safe, link_or_copy

__all__ = [
    "GlobalInstallResult",
    "install_global",
    "copy_directory_contents",
    "copy_file_safe",
    "link_or_copy",
]

