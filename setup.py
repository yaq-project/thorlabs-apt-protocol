#!/usr/bin/env python3

"""The setup script."""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

with open(here / "thorlabs_apt_protocol" / "VERSION") as version_file:
    version = version_file.read().strip()


with open("README.md") as readme_file:
    readme = readme_file.read()


extra_requirements = {"dev": ["black", "pre-commit"]}
extra_files = {"thorlabs_apt_protocol": ["VERSION"]}

setup(
    author="yaq Developers",
    author_email="git@ksunden.space",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    description="Functional implementation of the thorlabs APT protocol",
    extras_require=extra_requirements,
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data=extra_files,
    name="thorlabs-apt-protocol",
    packages=find_packages(
        include=["thorlabs_apt_protocol", "thorlabs_apt_protocol.*"]
    ),
    url="https://gitlab.com/yaq/thorlabs-apt-protocol",
    version=version,
    zip_safe=False,
)
