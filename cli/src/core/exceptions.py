"""Exception classes for the Dev-Team CLI engine."""


class DevTeamError(Exception):
    """Base exception for all Dev-Team errors."""


class ManifestError(DevTeamError):
    """Raised when an installation manifest cannot be parsed, created, or validated."""


class WorkspaceError(DevTeamError):
    """Raised when workspace detection, structure, or permissions fail."""


class PlatformError(DevTeamError):
    """Raised when a requested platform adapter is missing or invalid."""

