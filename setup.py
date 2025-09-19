from platform import python_version

from setuptools import setup, find_packages
from typing import Any

# Single source the version without importing the package
version_ns: dict[str, Any] = {}
with open("afs_fastapi/version.py", "r", encoding="utf-8") as _vf:
    exec(_vf.read(), version_ns)

# Ensure `version` is a plain str for setup() and satisfy static type-checkers
version: str = str(version_ns.get("__version__", "0.1.0"))

setup(
    name="afs_fastapi",
    version=version,
    packages=find_packages(),
    install_requires=[
        # List dependencies here, e.g., "fastapi", "pydantic"
        "fastapi",
        "pydantic",
        "uvicorn",
    ],
    python_requires=">=3.10, <3.13",
    author="D Deryl Downey",
    author_email="ddd@davidderyldowney.com",
    description="Automated Farming System API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="automated farming system fastapi afs_api",
    project_urls={
        "Bug Tracker": "https://github.com/dderyldowney/afs_fastapi/issues",
        "Documentation": "https://github.com/dderyldowney/afs_fastapi/blob/main/README.md",
        "Source Code": "https://github.com/dderyldowney/afs_fastapi",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: " + python_version(),
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "afs-api=afs_fastapi.__main__:main",
        ]
    },
)
