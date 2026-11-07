"""Dev-Team Core module: constants, provenance, hashing, and installation manifests."""

from .constants import (
    DEFAULT_VERSION,
    GLOBAL_HOME_DIR,
    GLOBAL_MANIFEST_FILE,
    PROJECT_MANIFEST_FILE,
    SUPPORTED_PLATFORMS,
)
from .exceptions import DevTeamError, ManifestError, WorkspaceError
from .manifest import Manifest, ManifestVerificationResult
from .provenance import compute_file_sha256, compute_directory_hashes

__all__ = [
    "DEFAULT_VERSION",
    "GLOBAL_HOME_DIR",
    "GLOBAL_MANIFEST_FILE",
    "PROJECT_MANIFEST_FILE",
    "SUPPORTED_PLATFORMS",
    "DevTeamError",
    "ManifestError",
    "WorkspaceError",
    "Manifest",
    "ManifestVerificationResult",
    "compute_file_sha256",
    "compute_directory_hashes",
]

