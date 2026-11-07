"""Installation manifest and provenance engine for Dev-Team."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .constants import (
    ALLOWED_INSTALLATION_MODES,
    ARTIFACT_TYPES,
    DEFAULT_INSTALLATION_MODE,
    DEFAULT_PLATFORM,
    DEFAULT_VERSION,
    STRATEGIES,
)
from .exceptions import ManifestError
from .provenance import compute_file_sha256


@dataclass
class ManifestArtifact:
    """Represents a single tracked file or projection managed by Dev-Team."""

    path: str
    type: str
    managed_by_dev_team: bool = True
    strategy: Optional[str] = None
    source: Optional[str] = None
    source_hash: Optional[str] = None
    user_modified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "path": self.path,
            "type": self.type,
            "managed_by_dev_team": self.managed_by_dev_team,
        }
        if self.strategy is not None:
            data["strategy"] = self.strategy
        if self.source is not None:
            data["source"] = self.source
        if self.source_hash is not None:
            data["source_hash"] = self.source_hash
        if self.user_modified:
            data["user_modified"] = self.user_modified
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ManifestArtifact:
        return cls(
            path=data["path"],
            type=data["type"],
            managed_by_dev_team=data.get("managed_by_dev_team", True),
            strategy=data.get("strategy"),
            source=data.get("source"),
            source_hash=data.get("source_hash"),
            user_modified=data.get("user_modified", False),
        )


@dataclass
class ManifestVerificationResult:
    """Outcome of verifying manifest entries against current on-disk state."""

    all_valid: bool
    total_artifacts: int
    intact_count: int
    missing_count: int
    modified_count: int
    missing_artifacts: List[str] = field(default_factory=list)
    modified_artifacts: List[str] = field(default_factory=list)
    intact_artifacts: List[str] = field(default_factory=list)
    details: List[Dict[str, Any]] = field(default_factory=list)


class Manifest:
    """In-memory representation and manager of a Dev-Team installation manifest."""

    def __init__(
        self,
        dev_team_version: str = DEFAULT_VERSION,
        installation_mode: str = DEFAULT_INSTALLATION_MODE,
        platform: str = DEFAULT_PLATFORM,
        installed_at: Optional[str] = None,
        artifacts: Optional[List[ManifestArtifact]] = None,
    ):
        self.dev_team_version = dev_team_version
        self.installation_mode = installation_mode
        self.platform = platform
        self.installed_at = installed_at or datetime.now(timezone.utc).isoformat()
        self.artifacts: List[ManifestArtifact] = artifacts or []

    def add_artifact(
        self,
        path: str,
        artifact_type: str,
        managed_by_dev_team: bool = True,
        strategy: Optional[str] = None,
        source: Optional[str] = None,
        source_hash: Optional[str] = None,
        user_modified: bool = False,
    ) -> ManifestArtifact:
        """Appends or updates a tracked artifact record."""
        # Normalize relative path to POSIX style for portability
        norm_path = Path(path).as_posix()
        if artifact_type not in ARTIFACT_TYPES:
            raise ManifestError(
                f"Invalid artifact type '{artifact_type}'. Allowed: {ARTIFACT_TYPES}"
            )
        if strategy is not None and strategy not in STRATEGIES:
            raise ManifestError(
                f"Invalid strategy '{strategy}'. Allowed: {STRATEGIES}"
            )

        # Remove existing if duplicate
        self.artifacts = [a for a in self.artifacts if a.path != norm_path]

        art = ManifestArtifact(
            path=norm_path,
            type=artifact_type,
            managed_by_dev_team=managed_by_dev_team,
            strategy=strategy,
            source=Path(source).as_posix() if source else None,
            source_hash=source_hash,
            user_modified=user_modified,
        )
        self.artifacts.append(art)
        return art

    def to_dict(self) -> Dict[str, Any]:
        """Converts manifest to a dictionary matching schemas/installation-manifest.schema.json."""
        return {
            "dev_team_version": self.dev_team_version,
            "installation_mode": self.installation_mode,
            "platform": self.platform,
            "installed_at": self.installed_at,
            "artifacts": [a.to_dict() for a in self.artifacts],
        }

    def validate_schema(self) -> List[str]:
        """Validates manifest dictionary against schema rules."""
        errors: List[str] = []
        if not self.dev_team_version:
            errors.append("Missing required field 'dev_team_version'")
        if self.installation_mode not in ALLOWED_INSTALLATION_MODES:
            errors.append(
                f"Invalid installation_mode '{self.installation_mode}'. Allowed: {ALLOWED_INSTALLATION_MODES}"
            )
        if not self.platform:
            errors.append("Missing required field 'platform'")
        if not self.installed_at:
            errors.append("Missing required field 'installed_at'")

        for idx, art in enumerate(self.artifacts):
            if not art.path:
                errors.append(f"artifacts[{idx}]: missing or empty 'path'")
            if art.type not in ARTIFACT_TYPES:
                errors.append(
                    f"artifacts[{idx}]: invalid type '{art.type}'. Allowed: {ARTIFACT_TYPES}"
                )
            if not isinstance(art.managed_by_dev_team, bool):
                errors.append(
                    f"artifacts[{idx}]: 'managed_by_dev_team' must be a boolean"
                )
            if art.strategy is not None and art.strategy not in STRATEGIES:
                errors.append(
                    f"artifacts[{idx}]: invalid strategy '{art.strategy}'. Allowed: {STRATEGIES}"
                )

        return errors

    def to_json(self, indent: int = 2) -> str:
        """Serializes manifest to JSON string."""
        errors = self.validate_schema()
        if errors:
            raise ManifestError(f"Cannot serialize invalid manifest: {errors}")
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, destination_path: Path) -> None:
        """Writes manifest JSON to disk at destination_path."""
        destination_path = Path(destination_path)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        content = self.to_json()
        with open(destination_path, "w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def load(cls, manifest_path: Path) -> Manifest:
        """Loads and validates a manifest file from disk."""
        manifest_path = Path(manifest_path)
        if not manifest_path.exists():
            raise ManifestError(f"Manifest file does not exist: {manifest_path}")

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise ManifestError(f"Failed to parse manifest JSON at {manifest_path}: {e}")

        artifacts = [ManifestArtifact.from_dict(item) for item in data.get("artifacts", [])]
        inst = cls(
            dev_team_version=data.get("dev_team_version", DEFAULT_VERSION),
            installation_mode=data.get("installation_mode", DEFAULT_INSTALLATION_MODE),
            platform=data.get("platform", DEFAULT_PLATFORM),
            installed_at=data.get("installed_at"),
            artifacts=artifacts,
        )

        validation_errors = inst.validate_schema()
        if validation_errors:
            raise ManifestError(
                f"Loaded manifest failed schema validation: {validation_errors}"
            )

        return inst

    def verify(self, base_directory: Path) -> ManifestVerificationResult:
        """
        Verifies every recorded artifact on disk against its recorded SHA-256 hash.
        Checks for missing files, modified files, and intact files.
        """
        base_dir = Path(base_directory)
        missing: List[str] = []
        modified: List[str] = []
        intact: List[str] = []
        details: List[Dict[str, Any]] = []

        for art in self.artifacts:
            art_path = base_dir / art.path
            detail: Dict[str, Any] = {
                "path": art.path,
                "type": art.type,
                "expected_hash": art.source_hash,
                "current_hash": None,
                "status": "UNKNOWN",
            }

            if not art_path.exists():
                missing.append(art.path)
                detail["status"] = "MISSING"
            elif art_path.is_file():
                current_hash = compute_file_sha256(art_path)
                detail["current_hash"] = current_hash
                if art.source_hash and current_hash != art.source_hash:
                    modified.append(art.path)
                    detail["status"] = "MODIFIED"
                else:
                    intact.append(art.path)
                    detail["status"] = "INTACT"
            elif art_path.is_dir():
                # Directory or projection symlink/junction
                intact.append(art.path)
                detail["status"] = "INTACT_DIR"

            details.append(detail)

        all_valid = (len(missing) == 0 and len(modified) == 0)
        return ManifestVerificationResult(
            all_valid=all_valid,
            total_artifacts=len(self.artifacts),
            intact_count=len(intact),
            missing_count=len(missing),
            modified_count=len(modified),
            missing_artifacts=missing,
            modified_artifacts=modified,
            intact_artifacts=intact,
            details=details,
        )

