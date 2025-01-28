from platform import python_version

from setuptools import setup, find_packages

setup(
    name="afs_fastapi",
    version="0.0.1-alpha",
    packages=find_packages(),
    install_requires=[
        # List dependencies here, e.g., "fastapi", "pydantic"
        "fastapi",
        "pydantic",
        "uvicorn",
    ],
    python_requires=">=3.8, <3.13",
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
)
