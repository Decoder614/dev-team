#!/usr/bin/env python3
"""Setup script for dev-team CLI package."""

from setuptools import setup, find_packages

setup(
    name="dev-team",
    version="1.1.0",
    description="Dev-Team CLI — Reusable AI-Assisted Software Development Toolkit",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    package_dir={
        "dev_team": "src",
        "dev_team.commands": "src/commands",
        "dev_team.core": "src/core",
        "dev_team.detection": "src/detection",
        "dev_team.installation": "src/installation",
        "dev_team.reporting": "src/reporting",
    },
    packages=[
        "dev_team",
        "dev_team.commands",
        "dev_team.core",
        "dev_team.detection",
        "dev_team.installation",
        "dev_team.reporting",
    ],
    install_requires=[
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "dev-team = dev_team.main:main",
        ],
    },
)

