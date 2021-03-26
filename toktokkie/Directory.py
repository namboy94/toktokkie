"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

This file is part of toktokkie.

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
LICENSE"""

import os
import json
import logging
from typing import List, Optional, Union, Type
from puffotter.prompt import yn_prompt
from toktokkie.metadata.base.Metadata import Metadata
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.metadata.book.Book import Book
from toktokkie.metadata.book_series.BookSeries import BookSeries
from toktokkie.metadata.comic.Comic import Comic
from toktokkie.metadata.music.Music import Music
from toktokkie.metadata.movie.Movie import Movie
from toktokkie.metadata.game.Game import Game
from toktokkie.enums import MediaType
from toktokkie.exceptions import MissingMetadata, InvalidMetadata
from puffotter.os import listdir


class Directory:
    """
    Class that encapsulates all of toktokkie's functionality
    """

    logger = logging.getLogger(__file__)
    """
    Logger for the directory class
    """

    def __init__(self, path: str, no_validation: bool = False):
        """
        Initializes the metadata of the directory
        :param path: The directory's path
        :param no_validation: Disables validation
        :except MissingMetadataException,
                InvalidMetadataException,
                MetadataMismatch
        """
        self.metadata = self.get_metadata(path, no_validation)

    @property
    def path(self) -> str:
        """
        :return: The path to the directory
        """
        return self.metadata.directory_path

    def reload(self):
        """
        Reloads the metadata from the metadata file
        :return: None
        """
        self.metadata = self.get_metadata(self.metadata.directory_path)

    def save(self):
        """
        Updates the metadata file with the current contents of the metadata
        :return: None
        """
        self.metadata.write()

    @classmethod
    def prompt(cls, path: str, metadata_type: Union[str, MediaType]) \
            -> Optional["Directory"]:
        """
        Prompts the user for metadata information
        :param path: The path to the directory for which to prompt
        :param metadata_type: The metadata type to generate
        :return: The generated directory, or None if aborted
        """
        try:
            existing: Optional[Directory] = Directory(path, True)
        except (InvalidMetadata, MissingMetadata):
            existing = None

        if existing is not None:
            prompt = yn_prompt("Metadata File already exists. "
                               "Continuing will delete the previous data. "
                               "Continue?")
            if not prompt:
                cls.logger.warning("Aborting")
                return None

        metadata = cls.create_metadata(path, metadata_type)
        metadata.write()
        return cls(path)

    @classmethod
    def load_directories(
            cls,
            paths: List[str],
            restrictions: Optional[List[MediaType]] = None,
            no_validation: bool = False
    ) -> List["Directory"]:
        """
        Loads the toktokkie Media Directory objects based on paths
        :param paths: The directories to turn into toktokkie Directory objs
        :param restrictions: Restricts the found media directories to media
                             directories with a specific media type
        :param no_validation: Whether or not to validate metadata
        :return: The list of Media Directories
        """
        if restrictions is None:
            restrictions = [x for x in MediaType]

        logger = logging.getLogger(cls.__name__)

        directories = []  # type: List[Directory]
        for path in paths:
            try:
                logger.debug("Loading directory {}".format(path))
                directory = Directory(path, no_validation=no_validation)
                if directory.metadata.media_type() not in restrictions:
                    logger.info(
                        "Skipping directory {} with incorrect type {}"
                        .format(path, directory.metadata.media_type())
                    )
                    continue
                directories.append(directory)

            except MissingMetadata:
                logger.warning("{} has no metadata file.".format(path))
            except InvalidMetadata as e:
                logger.warning("{}'s metadata is invalid.".format(path))
                logger.warning(e.reason)

        return directories

    @classmethod
    def load_child_directories(
            cls,
            parent_dir: str,
            restrictions: Optional[List[MediaType]] = None,
            no_validation: bool = False
    ) -> List["Directory"]:
        """
        Loads all media directories in a directory
        :param parent_dir: The directory to search for media directories
        :param restrictions: Restricts the found media directories to media
                             directories with a specific media type
        :param no_validation: Whether or not to validate metadata
        :return: The list of Media Directories
        """
        paths = [x[1] for x in listdir(parent_dir)]
        return cls.load_directories(paths, restrictions)

    @staticmethod
    def get_metadata(directory: str, no_validation: bool = False) -> Metadata:
        """
        Automatically resolves the metadata of a directory
        :param directory: The directory for which to generate the metadata
        :param no_validation: Disables Validation
        :return: The generated metadata
        :raises InvalidMetadataException: If the metadata is invalid
        """
        info_file = os.path.join(directory, ".meta/info.json")
        try:
            with open(info_file, "r") as f:
                media_type = json.load(f)["type"]
                metadata_cls = Directory.get_metadata_class(media_type)
                return metadata_cls(directory, no_validation=no_validation)
        except (KeyError, ValueError) as e:
            raise InvalidMetadata(f"Missing/Invalid attribute: {e}")
        except FileNotFoundError:
            raise MissingMetadata()
        except NotADirectoryError:
            raise MissingMetadata("Not a directory")

    @staticmethod
    def create_metadata(directory: str, media_type: Union[str, MediaType]) \
            -> Metadata:
        """
        Generates a new metadata object using user prompts
        :param directory: The directory for which to generate the metadata
        :param media_type: The media type of the metadata
        :return: The generated metadata
        """
        metadata_cls = Directory.get_metadata_class(media_type)
        metadata = metadata_cls.from_prompt(directory)
        metadata.write()
        return metadata

    @staticmethod
    def get_metadata_class(media_type: Union[str, MediaType]) \
            -> Type[Metadata]:
        """
        Retrieves the metadata class for a given media type
        :param media_type: The media type for which to get the metadata class
        :return: The metadata class
        """
        if isinstance(media_type, str):
            media_type = MediaType(media_type)

        mapping = {
            x.media_type(): x
            for x in [
                Book,
                BookSeries,
                Comic,
                Movie,
                Tv,
                Music,
                Game
            ]
        }
        return mapping[media_type]
