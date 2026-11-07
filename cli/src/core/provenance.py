"""Provenance and hashing engine for artifact tracking and drift detection."""

import hashlib
from pathlib import Path
from typing import Dict


def compute_file_sha256(file_path: Path) -> str:
    """Computes the SHA-256 hexadecimal digest of a file in 64KB blocks."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def compute_directory_hashes(directory: Path) -> Dict[str, str]:
    """
    Computes SHA-256 hashes for all regular files within a directory tree.
    Returns mapping of normalized POSIX relative path to SHA-256 hash.
    """
    hashes: Dict[str, str] = {}
    if not directory.exists() or not directory.is_dir():
        return hashes

    for path in directory.rglob("*"):
        if path.is_file():
            rel_path = path.relative_to(directory).as_posix()
            hashes[rel_path] = compute_file_sha256(path)

    return hashes

