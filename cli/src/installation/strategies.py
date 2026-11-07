"""Filesystem manipulation strategies: copying, symlinking, and directory junctions."""

import os
import shutil
import sys
from pathlib import Path
from typing import Tuple


def copy_file_safe(src: Path, dst: Path) -> Path:
    """Copies a single file from src to dst, ensuring parent directories exist."""
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def copy_directory_contents(src_dir: Path, dst_dir: Path) -> int:
    """
    Recursively copies all files and subdirectories from src_dir into dst_dir.
    Returns the count of copied files.
    """
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    if not src_dir.exists() or not src_dir.is_dir():
        return 0

    count = 0
    for item in src_dir.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src_dir)
            target = dst_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            count += 1
    return count


def link_or_copy(src_dir: Path, dst_dir: Path, preferred_mode: str = "copy") -> Tuple[str, str]:
    """
    Attempts to link src_dir to dst_dir using preferred strategy (symlink, junction, copy).
    Falls back gracefully if privileges or filesystem support is missing.
    Returns (actual_strategy_used, message).
    """
    src_dir = Path(src_dir).resolve()
    dst_dir = Path(dst_dir)
    is_win = sys.platform.startswith("win")

    # If copy was explicitly requested or fallback
    if preferred_mode == "copy":
        copy_directory_contents(src_dir, dst_dir)
        return "copy", "Copied files directly"

    # Symlink attempt
    if preferred_mode == "symlink":
        try:
            if dst_dir.exists() or dst_dir.is_symlink():
                if dst_dir.is_symlink() or (is_win and hasattr(dst_dir, "is_junction") and dst_dir.is_junction()):
                    dst_dir.unlink()
                else:
                    shutil.rmtree(dst_dir)
            dst_dir.symlink_to(src_dir, target_is_directory=True)
            return "symlink", "Created directory symlink"
        except (OSError, NotImplementedError) as e:
            if is_win:
                # Windows fallback to NTFS junction
                try:
                    import subprocess
                    cmd = f'mklink /J "{dst_dir}" "{src_dir}"'
                    subprocess.run(cmd, shell=True, check=True, capture_output=True)
                    return "junction", "Created NTFS directory junction"
                except Exception:
                    pass

    # Final safe fallback: Copy
    copy_directory_contents(src_dir, dst_dir)
    return "copy", "Fell back to safe copy strategy"

