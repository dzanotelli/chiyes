"""
A python wrapper for chino.io API

(C) 2019 Daniele Zanotelli

"""

import subprocess

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def get_version():
    proc = subprocess.run(["git", "describe"], capture_output=True)
    if proc.returncode is 0:
        return proc.stdout
    return "unknown"


# get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# read requirements.txt file
with open(path.join(here, 'requirements.txt'), 'r') as f:
    required_all = f.read().strip().split('\n')

required_dev = ['ipython', 'sphinx_rtd_theme']
required = [item for item in required_all if item not in required_dev]

setup(
    name="chiyes",
    version=get_version(),
    description="Unofficial wrapper for chino.io API.",
    long_description=long_description,
    url="https://github.com/dzanotelli/chiyes",
    author="Daniele Zanotelli",
    author_email="dazano@gmail.com",
    license="MIT",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
    ],

    keywords="chino.io api wrapper sdk",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=required,
    python_requires='>=3.7',

    extras_require={
        'dev': [],
    },

    package_data={},
    entry_points={},
)
