"""Detection module for Dev-Team: workspace inspection, git detection, and platforms."""

from .platform import (
    PlatformInfo,
    ToolInfo,
    detect_all_platforms,
    detect_platform_readiness,
    detect_system_tools,
)
from .workspace import (
    WorkspaceInfo,
    detect_existing_configuration,
    detect_workspace,
    detect_workspace_type,
    find_canonical_source_repo,
    find_git_root,
)

__all__ = [
    "PlatformInfo",
    "ToolInfo",
    "detect_all_platforms",
    "detect_platform_readiness",
    "detect_system_tools",
    "WorkspaceInfo",
    "detect_existing_configuration",
    "detect_workspace",
    "detect_workspace_type",
    "find_canonical_source_repo",
    "find_git_root",
]

