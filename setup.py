"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from setuptools import setup, find_packages
import media_manager.metadata as metadata


def readme() -> str:
    """
    Reads the readme file.

    :return: the readme file as a string
    """
    try:
        # noinspection PyPackageRequirements
        import pypandoc
        with open('README.md') as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, 'rst', format='md')
            return rst
    except (OSError, ImportError):
        # If pandoc is not installed, just return the raw markdown text
        with open('README.md') as f:
            return f.read()


setup(name=metadata.project_name,
      version=metadata.version_number,
      description=metadata.project_description,
      long_description=readme(),
      classifiers=[metadata.development_status,
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3',
                   'Topic :: Utilities',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux'
                   ],
      url=metadata.project_url,
      download_url=metadata.download_url,
      author=metadata.author_name,
      author_email=metadata.author_email,
      license=metadata.license_type,
      packages=find_packages(),
      install_requires=['tvdb_api', 'beautifulsoup4', 'gfworks', 'twisted', 'typing', 'irc'],
      dependency_links=['https://git.gnome.org/browse/pygobject'],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/mediamanager', 'bin/mediamanager-gtk', 'bin/mediamanager-tk'],
      zip_safe=False)

# How to upload to pypi:
# python setup.py register sdist upload
