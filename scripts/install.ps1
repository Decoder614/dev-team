<#
.SYNOPSIS
    Installs, links, or uninstalls Dev-Team skills for OpenAI Codex CLI on Windows.

.DESCRIPTION
    Dev-Team installer script for Windows. Discovers skills in the Dev-Team repository
    and either copies or links (symlink/junction) them into the user-level Codex skills
    directory (~/.codex/skills) or a specified target repository.

.PARAMETER Mode
    Installation mode: 'Copy' (default, independent copy) or 'Symlink' (symbolic link/junction).

.PARAMETER CodexDir
    Custom path to the Codex skills directory. Defaults to $env:CODEX_HOME\skills
    or $env:USERPROFILE\.codex\skills.

.PARAMETER TargetRepo
    Path to an application repository. When specified, installs skills to
    <TargetRepo>\.codex\skills and scaffolds the .dev-team directory.

.PARAMETER Uninstall
    Removes previously installed Dev-Team skills while strictly preserving unrelated user skills.

.PARAMETER Force
    Overwrites existing target skill directories without prompting.

.PARAMETER DryRun
    Simulates the installation or uninstallation without making filesystem modifications.

.PARAMETER Help
    Displays usage and help information.

.EXAMPLE
    .\install.ps1
    Installs all Dev-Team skills to user-level ~/.codex/skills via Copy mode.

.EXAMPLE
    .\install.ps1 -Mode Symlink
    Links all Dev-Team skills into ~/.codex/skills using junctions or symlinks.

.EXAMPLE
    .\install.ps1 -TargetRepo "E:\apps\my-project"
    Installs skills into a specific application repository.

.EXAMPLE
    .\install.ps1 -Uninstall
    Safely removes only Dev-Team skills from ~/.codex/skills.
#>

[CmdletBinding(DefaultParameterSetName = "Install")]
param(
    [Parameter(ParameterSetName = "Install")]
    [ValidateSet("Copy", "Symlink")]
    [string]$Mode = "Copy",

    [Parameter(ParameterSetName = "Install")]
    [Parameter(ParameterSetName = "Uninstall")]
    [string]$CodexDir,

    [Parameter(ParameterSetName = "Install")]
    [string]$TargetRepo,

    [Parameter(ParameterSetName = "Uninstall", Mandatory = $true)]
    [switch]$Uninstall,

    [Parameter()]
    [switch]$Force,

    [Parameter()]
    [switch]$DryRun,

    [Parameter()]
    [switch]$Help
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Full
    exit 0
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "             Dev-Team Installer for Windows                 " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Resolve Dev-Team root directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DevTeamRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$SourceSkillsDir = Join-Path $DevTeamRoot "skills"

if (-not (Test-Path $SourceSkillsDir -PathType Container)) {
    Write-Error "[FAIL] Source skills directory not found at: $SourceSkillsDir"
    exit 1
}

# Discover all valid skills in dev-team (directories containing SKILL.md)
$DiscoveredSkills = Get-ChildItem -Path $SourceSkillsDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "SKILL.md")
}

if ($DiscoveredSkills.Count -eq 0) {
    Write-Error "[FAIL] No valid skills found in $SourceSkillsDir (must contain SKILL.md)"
    exit 1
}

Write-Host "Dev-Team Root : $DevTeamRoot"
Write-Host "Source Skills : $SourceSkillsDir ($($DiscoveredSkills.Count) skills found)"

# 1.1 Verify CLI environment and configure Windows User PATH
$CliDir = Join-Path $DevTeamRoot "cli"
if (Test-Path $CliDir) {
    try {
        $pyUserBase = python -c "import os, sys, site; print(os.path.join(site.USER_BASE, f'Python{sys.version_info.major}{sys.version_info.minor}', 'Scripts'))" 2>$null
        if ($pyUserBase -and (Test-Path $pyUserBase)) {
            $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
            $paths = $userPath.Split(';') | Where-Object { $_ -ne "" }
            if ($paths -notcontains $pyUserBase) {
                $newPath = ($paths + $pyUserBase) -join ';'
                [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
                $env:PATH += ";$pyUserBase"
                Write-Host "  [PATH] Automatically added Python user Scripts directory to Windows User PATH: $pyUserBase" -ForegroundColor Green
            }
        }
    } catch {
        # Non-blocking PATH check
    }
}

# 2. Determine Destination Skills Directory
if ($TargetRepo) {
    if (-not (Test-Path $TargetRepo -PathType Container)) {
        Write-Error "[FAIL] Specified TargetRepo directory does not exist: $TargetRepo"
        exit 1
    }
    $ResolvedTargetRepo = (Resolve-Path $TargetRepo).Path
    $DestSkillsDir = Join-Path $ResolvedTargetRepo ".codex\skills"
    Write-Host "Target Mode   : Target Repository ($ResolvedTargetRepo)"
} elseif ($CodexDir) {
    $DestSkillsDir = $CodexDir
    Write-Host "Target Mode   : Custom Directory ($DestSkillsDir)"
} else {
    if ($env:CODEX_HOME) {
        $DestSkillsDir = Join-Path $env:CODEX_HOME "skills"
    } else {
        $DestSkillsDir = Join-Path $env:USERPROFILE ".codex\skills"
    }
    Write-Host "Target Mode   : User-Level Codex Skills ($DestSkillsDir)"
}

Write-Host "Destination   : $DestSkillsDir"
if ($DryRun) {
    Write-Host "[DRY-RUN] No filesystem modifications will be made." -ForegroundColor Yellow
}
Write-Host "------------------------------------------------------------"

# 3. Handle Uninstallation
if ($Uninstall) {
    Write-Host "Starting uninstallation of Dev-Team skills..." -ForegroundColor Yellow
    $RemovedCount = 0
    $SkippedCount = 0

    if (-not (Test-Path $DestSkillsDir)) {
        Write-Host "Destination directory does not exist. Nothing to uninstall." -ForegroundColor Green
        exit 0
    }

    foreach ($skill in $DiscoveredSkills) {
        $skillName = $skill.Name
        $targetSkillPath = Join-Path $DestSkillsDir $skillName

        if (Test-Path $targetSkillPath) {
            Write-Host "  -> Removing Dev-Team skill: $skillName"
            if (-not $DryRun) {
                # Handle junctions/symlinks vs directories
                $item = Get-Item -LiteralPath $targetSkillPath -Force
                if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                    # Reparse point (symlink or junction)
                    [System.IO.Directory]::Delete($targetSkillPath)
                } else {
                    Remove-Item -LiteralPath $targetSkillPath -Recurse -Force
                }
            }
            $RemovedCount++
        } else {
            $SkippedCount++
        }
    }

    Write-Host "------------------------------------------------------------"
    Write-Host "Uninstallation Summary:" -ForegroundColor Green
    Write-Host "  Skills Removed : $RemovedCount"
    Write-Host "  Not Found/Skip : $SkippedCount"
    Write-Host "  Unrelated skills in destination were preserved."
    exit 0
}

# 4. Handle Installation
Write-Host "Starting installation (Mode: $Mode)..." -ForegroundColor Green

if (-not (Test-Path $DestSkillsDir) -and -not $DryRun) {
    New-Item -Path $DestSkillsDir -ItemType Directory -Force | Out-Null
    Write-Host "Created destination skills directory: $DestSkillsDir"
}

# If TargetRepo mode, also scaffold .dev-team directory if not present
if ($TargetRepo -and -not $DryRun) {
    $devTeamDir = Join-Path $ResolvedTargetRepo ".dev-team"
    $featuresDir = Join-Path $devTeamDir "features"
    if (-not (Test-Path $featuresDir)) {
        New-Item -Path $featuresDir -ItemType Directory -Force | Out-Null
        Write-Host "Scaffolded target directory: $featuresDir"
    }
}

$InstalledCount = 0
$UpdatedCount = 0
$SkippedCount = 0
$FailedCount = 0

foreach ($skill in $DiscoveredSkills) {
    $skillName = $skill.Name
    $srcPath = $skill.FullName
    $destPath = Join-Path $DestSkillsDir $skillName

    try {
        if ($Mode -eq "Copy") {
            $exists = Test-Path $destPath
            if ($exists -and -not $Force) {
                # Check if it needs updating or is already present
                Write-Host "  [UPDATE] Updating existing skill: $skillName"
                if (-not $DryRun) {
                    Copy-Item -Path $srcPath -Destination $DestSkillsDir -Recurse -Force
                }
                $UpdatedCount++
            } else {
                Write-Host "  [INSTALL] Copying skill: $skillName"
                if (-not $DryRun) {
                    Copy-Item -Path $srcPath -Destination $DestSkillsDir -Recurse -Force
                }
                $InstalledCount++
            }
        } elseif ($Mode -eq "Symlink") {
            $exists = Test-Path $destPath
            if ($exists) {
                $item = Get-Item -LiteralPath $destPath -Force
                $isReparse = ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
                if ($isReparse) {
                    Write-Host "  [SKIP] Link already exists for: $skillName"
                    $SkippedCount++
                    continue
                } elseif ($Force) {
                    Write-Host "  [REPLACE] Removing existing directory to create link: $skillName"
                    if (-not $DryRun) {
                        Remove-Item -LiteralPath $destPath -Recurse -Force
                    }
                } else {
                    Write-Host "  [WARN] Regular directory already exists at target: $skillName (use -Force to replace with link)" -ForegroundColor Yellow
                    $SkippedCount++
                    continue
                }
            }

            Write-Host "  [LINK] Creating link for skill: $skillName"
            if (-not $DryRun) {
                # Attempt symbolic link first; fallback to directory junction if Developer Mode is off
                try {
                    New-Item -Path $destPath -ItemType SymbolicLink -Target $srcPath -ErrorAction Stop | Out-Null
                } catch {
                    # Fallback to junction
                    New-Item -Path $destPath -ItemType Junction -Target $srcPath -ErrorAction Stop | Out-Null
                }
            }
            $InstalledCount++
        }
    } catch {
        Write-Host "  [FAIL] Error processing skill $skillName : $_" -ForegroundColor Red
        $FailedCount++
    }
}

Write-Host "------------------------------------------------------------"
Write-Host "Installation Summary:" -ForegroundColor Cyan
Write-Host "  New Skills Installed : $InstalledCount"
Write-Host "  Skills Updated       : $UpdatedCount"
Write-Host "  Skills Skipped       : $SkippedCount"
Write-Host "  Skills Failed        : $FailedCount"

if ($FailedCount -gt 0) {
    Write-Host "[RESULT] Installation finished with errors." -ForegroundColor Red
    exit 1
}

Write-Host "[RESULT] Dev-Team skills successfully configured!" -ForegroundColor Green
exit 0

