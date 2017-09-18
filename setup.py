"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import json
from toktokkie.metadata import version
from setuptools import setup, find_packages


def readme():
    """
    Reads the readme file.

    :return: the readme file as a string
    """
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements
        import pypandoc
        with open('README.md') as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, 'rst', format='md')
            return rst
    except:
        # If pandoc is not installed, just return the raw markdown text
        with open('README.md') as f:
            return f.read()


def find_scripts():
    """
    Returns a list of scripts in the bin directory

    :return: the list of scripts
    """
    try:
        scripts = []
        for file_name in os.listdir("bin"):
            if not file_name == "__init__.py" and os.path.isfile(os.path.join("bin", file_name)):
                scripts.append(os.path.join("bin", file_name))
        return scripts
    except OSError:
        return []


def create_local_config_dir():
    """
    Creates alocal configuration directory with default values if none exist yet
    
    :return: None
    """
    toktokkie_dir = os.path.join(os.path.expanduser("~"), ".toktokkie")
    if not os.path.isdir(toktokkie_dir):
        os.makedirs(toktokkie_dir)

    metadata_config_file = os.path.join(toktokkie_dir, "metadata_config.json")
    if not os.path.isfile(metadata_config_file):
        with open(metadata_config_file, 'w') as f:
            f.write(json.dumps({"media_directories": []}))


create_local_config_dir()
setup(name="toktokkie",
      version=version,
      description="A personal media manager program",
      long_description=readme(),
      classifiers=[
        "Environment :: Other Environment",
        "Natural Language :: English",
        "Intended Audience :: End Users/Desktop",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
      ],
      url="https://gitlab.namibsun.net/namboy94/toktokkie",
      download_url="https://gitlab.namibsun.net/namboy94/toktokkie/repository/archive.zip?ref=master",
      author="Hermann Krumrey",
      author_email="hermann@krumreyh.com",
      license="GNU GPL3",
      packages=find_packages(),
      install_requires=['tvdb_api', 'beautifulsoup4', 'typing', 'raven', 'urwid', 'xdcc_dl'],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=find_scripts(),
      zip_safe=False)
