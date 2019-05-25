# -*- coding: utf-8 -*-

"""
pdfgeneratorapi
~~~~~~~
Setup for PDFGeneratorAPI
"""

from setuptools import setup, find_packages

setup(
    name="pdfgeneratorapi",
    version="0.1",
    description="A python client library for PDFGeneratorAPI.com",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/sameerkumar18/pdfgeneratorapi-python",
    author="Sameer Kumar",
    author_email="sam@sameerkumar.website",
    license="Apache 2.0",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="api wrapper client library pdfgeneratorapi pdfgenerator",
    packages=find_packages(exclude=["contrib", "docs", "tests", "venv"]),
    install_requires=["requests", "python-dateutil"],
    test_suite="tests",
    test_require=["python-dotenv"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev]
    extras_require={"dev": ["sphinx", "sphinx-autobuild"]},
)
