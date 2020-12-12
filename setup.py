#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proxpy",
    version="1.0.1",
    author="Nick Demers",
    description="A simple utility for generating sheets of MtG proxies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demern/proxpy",
    scripts=['bin/proxpy'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "appdirs",
        "Pillow",
        "requests"
    ],
    python_requires='>=3.6',
)
