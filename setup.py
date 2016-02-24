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
from setuptools import setup


def readme():
    """
    Reads the readme file.
    :return: the readme file as a string
    """
    with open('README.md') as f:
        return f.read()


setup(name='media-manager',
      version='0.7.3',
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
      packages=['media_manager',
                'media_manager.external',
                'media_manager.guitemplates',
                'media_manager.guitemplates.gtk',
                'media_manager.guitemplates.tk',
                'media_manager.mainuserinterfaces',
                'media_manager.plugins',
                'media_manager.plugins.batchdownloadmanager',
                'media_manager.plugins.batchdownloadmanager.downloaders',
                'media_manager.plugins.batchdownloadmanager.searchengines',
                'media_manager.plugins.batchdownloadmanager.searchengines.objects',
                'media_manager.plugins.batchdownloadmanager.userinterfaces',
                'media_manager.plugins.batchdownloadmanager.utils',
                'media_manager.plugins.common',
                'media_manager.plugins.common.fileops',
                'media_manager.plugins.common.onlinedatagetters',
                'media_manager.plugins.iconizer',
                'media_manager.plugins.iconizer.userinterfaces',
                'media_manager.plugins.iconizer.utils',
                'media_manager.plugins.iconizer.utils.iconizers',
                'media_manager.plugins.renamer',
                'media_manager.plugins.renamer.objects',
                'media_manager.plugins.renamer.userinterfaces',
                'media_manager.plugins.renamer.utils',
                'media_manager.startup'],
      install_requires=['tvdb_api', 'beautifulsoup4'],
      dependency_links=['https://git.gnome.org/browse/pygobject'],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/mediamanager', 'bin/mediamanager-gtk', 'bin/mediamanager-tk'],
      zip_safe=False)

# How to upload to pypi:
# python setup.py register sdist upload
