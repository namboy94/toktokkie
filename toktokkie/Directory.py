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
import sys
import logging
from typing import Dict, Any, List, Optional
from puffotter.prompt import yn_prompt
from toktokkie.renaming.Renamer import Renamer
from toktokkie.iconizing.Iconizer import Iconizer, Procedure
from toktokkie.metadata.functions import get_metadata, create_metadata
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.MediaType import MediaType
from toktokkie.exceptions import MissingMetadata, InvalidUpdateInstructions, \
    MissingUpdateInstructions, InvalidMetadata
from toktokkie.update import updaters
from toktokkie.check.map import checker_map
from puffotter.os import listdir


class Directory:
    """
    Class that encapsulates all of toktokkie's functionality
    """

    def __init__(self, path: str, generate_metadata: bool = False,
                 metadata_type: str = None):
        """
        Initializes the metadata of the directory
        :param path: The directory's path
        :except MissingMetadataException,
                InvalidMetadataException,
                MetadataMismatch
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.path = path
        self.meta_dir = os.path.join(path, ".meta")
        self.metadata_file = os.path.join(self.meta_dir, "info.json")

        if generate_metadata:

            if metadata_type is None:
                raise ValueError("Metadata type must be specified")
            self.generate_metadata(metadata_type)

        if not os.path.isfile(self.metadata_file):
            raise MissingMetadata(self.metadata_file + " missing")

        self.metadata = get_metadata(self.path)  # type: Metadata

        if not os.path.isdir(self.metadata.icon_directory):
            os.makedirs(self.metadata.icon_directory)

    def reload(self):
        """
        Reloads the metadata from the metadata file
        :return: None
        """
        self.metadata = get_metadata(self.path)

    def write_metadata(self):
        """
        Updates the metadata file with the current contents of the metadata
        :return: None
        """
        self.metadata.write()

    def generate_metadata(self, metadata_type: str):
        """
        Prompts the user for metadata information
        :param metadata_type: The metadata type to generate
        :return: None
        """

        if os.path.isfile(self.metadata_file):
            prompt = yn_prompt("Metadata File already exists. "
                               "Continuing will delete the previous data. "
                               "Continue?")
            if not prompt:
                self.logger.warning("Aborting")
                sys.exit(0)

        metadata = create_metadata(self.path, metadata_type)
        metadata.write()

    def rename(self, noconfirm: bool = False):
        """
        Renames the contained files.
        :param noconfirm: Skips the confirmation phase
        :return: None
        """
        Renamer(self.metadata).rename(noconfirm)
        self.path = self.metadata.directory_path

    def iconize(self, procedure: Procedure):
        """
        Applies the directory's icons
        :param procedure: The iconizing procedure to use
        :return: None
        """
        iconizer = Iconizer(self.path, self.metadata.icon_directory, procedure)
        iconizer.iconize()

    def check(
            self,
            show_warnings: bool,
            fix_interactively: bool,
            config: Dict[str, Any]
    ) -> bool:
        """
        Performs a check, making sure that everything in the directory
        is configured correctly and up-to-date
        :param show_warnings: Whether or not to show warnings
        :param fix_interactively: Whether or not to enable interactive fixing
        :param config: Configuration dictionary for checks
        :return: The check result
        """
        checker_cls = checker_map[self.metadata.media_type()]
        checker = checker_cls(
            self.metadata,
            show_warnings,
            fix_interactively,
            config
        )
        return checker.check()

    def update(self, args: Dict[str, Any]):
        """
        Performs an Update Action
        :param args: Command line arguments used to configure the update
        :return: None
        """
        applicable_updaters = [
            x for x in updaters
            if self.metadata.media_type() in x.applicable_media_types()
        ]
        for updater_cls in applicable_updaters:

            if args["create"]:
                updater_cls.prompt(self.metadata)
            else:
                try:
                    updater = updater_cls(self.metadata, args)
                    print("Updating {} using {} updater:".format(
                        self.metadata.name, updater.name()
                    ))
                    updater.update()
                except MissingUpdateInstructions:
                    self.logger.warning("No update instructions for {}"
                                        .format(self.path))
                except InvalidUpdateInstructions as e:
                    self.logger.warning(
                        "Update instructions for {} are invalid: {}"
                        .format(self.path, e)
                    )

    @classmethod
    def load_directories(
            cls,
            paths: List[str],
            restrictions: Optional[List[MediaType]] = None
    ) -> List["Directory"]:
        """
        Loads the toktokkie Media Directory objects based on paths
        :param paths: The directories to turn into toktokkie Directory objs
        :param restrictions: Restricts the found media directories to media
                             directories with a specific media type
        :return: The list of Media Directories
        """
        if restrictions is None:
            restrictions = [x for x in MediaType]

        logger = logging.getLogger(cls.__name__)

        directories = []  # type: List[Directory]
        for path in paths:
            try:
                logger.debug("Loading directory {}".format(path))
                directory = Directory(path)
                if directory.metadata.media_type() not in restrictions:
                    logger.info(
                        "Skipping directory {} with incorrect type {}"
                        .format(path, directory.metadata.media_type())
                    )
                    continue
                directories.append(directory)

            except MissingMetadata:
                logger.warning("{} has no metadata file.".format(path))
            except InvalidMetadata:
                logger.warning("{}'s metadata is invalid.".format(path))

        return directories

    @classmethod
    def load_child_directories(
            cls,
            parent_dir: str,
            restrictions: Optional[List[MediaType]] = None
    ) -> List["Directory"]:
        """
        Loads all media directories in a directory
        :param parent_dir: The directory to search for media directories
        :param restrictions: Restricts the found media directories to media
                             directories with a specific media type
        :return: The list of Media Directories
        """
        paths = [x[1] for x in listdir(parent_dir)]
        return cls.load_directories(paths, restrictions)
