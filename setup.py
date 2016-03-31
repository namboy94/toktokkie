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


def readme():
    """
    Reads the readme file.
    :return: the readme file as a string
    """
    with open('README.md') as f:
        return f.read()


setup(name='media-manager',
      version='0.8.4',
      description='A personal media manager program',
      long_description=readme(),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3',
                   'Topic :: Utilities',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux'
                   ],
      url='http://namibsun.net/namboy94/media-manager',
      author='Hermann Krumrey',
      author_email='hermann@krumreyh.com',
      license='GNU GPL3',
      packages=find_packages(),
      install_requires=['tvdb_api', 'beautifulsoup4', 'gfworks'],
      dependency_links=['https://git.gnome.org/browse/pygobject'],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/mediamanager', 'bin/mediamanager-gtk', 'bin/mediamanager-tk'],
      zip_safe=False)

# How to upload to pypi:
# python setup.py register sdist upload
