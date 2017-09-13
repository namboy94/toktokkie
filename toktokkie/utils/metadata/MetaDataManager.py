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
from typing import List, Dict
from toktokkie.utils.metadata.MediaTypes import MediaTypes


class MetaDataManager(object):
    """
    Class that handles the metadata for Media files
    """

    @staticmethod
    def find_recursive_media_directories(directory: str, media_type: str = "") -> List[str]:
        """
        Finds all directories that include a .meta directory below a given
        directory. If a media_type is specified, only those directories containing a .meta/type file
        with the media_type as content are considered

        In case the given directory does not exist or the current user has no read access,
        an empty list is returned

        :param directory:  The directory to check
        :param media_type: The media type to check for
        :return:           A list of directories that are identified as TV Series
        """
        directories = []

        if not os.path.isdir(directory):
            return []

        # noinspection PyUnboundLocalVariable
        try:
            children = os.listdir(directory)
        except (OSError, IOError):  # == PermissionError
            # If we don't have read permissions for this directory, skip this directory
            return []

        if MetaDataManager.is_media_directory(directory, media_type):
            directories.append(directory)
        else:
            # Parse every subdirectory like the original directory recursively
            for child in children:
                child_path = os.path.join(directory, child)
                if os.path.isdir(child_path):
                    directories += MetaDataManager.find_recursive_media_directories(child_path, media_type)

        return directories

    @staticmethod
    def is_media_directory(directory: str, media_type: str = "") -> bool:
        """
        Checks if a given directory is a Media directory.
        A directory is a Media directory when it contains a .meta directory. It will also contain
        a info.json file which specifies the type of the media as well as other metadata

        :param directory:  The directory to check
        :param media_type: The type of media to check for, optional
        :return:           True if the directory is a Media directory, False otherwise
        """
        # noinspection PyUnboundLocalVariable
        try:
            if ".meta" in os.listdir(directory):

                if media_type:
                    return MetaDataManager.is_media_subtype(directory, media_type)
                else:
                    return True

            else:
                return False

        except (OSError, IOError, KeyError):  # Permission Errors or Missing type in info.json (if type specified)
            return False

    @staticmethod
    def generate_media_directory(directory: str, media_type: str = "generic") -> None:
        """
        Makes sure a directory is a media directory of the given type

        :param directory:  The directory
        :param media_type: The media type, if not supplied will default to 'generic'
        :raises:           IOError (FileExistsError), if the file exists and is not a directory
        :return:           None
        """
        if not os.path.isdir(directory):
            if os.path.isfile(directory):
                raise IOError("Directory already exists and is a File?")
            else:
                os.makedirs(directory)

        if not MetaDataManager.is_media_directory(directory, media_type):

            for path in [directory, os.path.join(directory, ".meta", "icons")]:
                if not os.path.isdir(path):
                    os.makedirs(path)

            info_data = MediaTypes.generate_basic_info_data(media_type)
            MetaDataManager.set_media_info(directory, info_data)

    @staticmethod
    def get_media_type(directory: str) -> str:
        """
        Determines the media type of a media directory

        :param directory: The directory to check
        :return:          Either the type identifier string, or an empty string
                          if the directory is not a media directory
        """
        try:
            return str(MetaDataManager.get_media_info(directory)["type"])
        except KeyError:
            return ""

    @staticmethod
    def is_media_subtype(directory: str, media_type: str) -> bool:
        """
        Checks if a directory is of a specific media type of subtype.

        Example of a subtype: anime_series is a subtype of tv_series

        :param directory: The directory to check
        :param media_type: The media type/subtype to check
        :return: True if the media directory corresponds to the given type
        """
        return MediaTypes.is_subtype_of(MetaDataManager.get_media_type(directory), media_type)

    @staticmethod
    def get_media_info(directory: str) -> Dict[str, object]:
        """
        Retrieves the stored information in a media directory's info.json file

        :param directory: The media directory to check
        :return: The JSON data of that file. Guaranteed to have a 'type' attribute
        """

        info_file = os.path.join(directory, ".meta", "info.json")

        if not os.path.isfile(info_file):
            return {}
        else:
            with open(info_file, 'r') as json_file:
                return json.loads(json_file.read())

    @staticmethod
    def set_media_info(directory: str, data: Dict[str, object]) -> None:
        """
        Sets the info.json data for a media directory. Overwrites the old data!

        :param directory: The media directory for which to write the info data
        :param data: The data to write to the info.json file
        :return: None
        """
        with open(os.path.join(directory, ".meta", "info.json"), "w") as info_file:
            json_data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            info_file.write(json_data)
