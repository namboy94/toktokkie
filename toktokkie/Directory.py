"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

import os
import sys
from toktokkie.renaming import Renamer
from toktokkie.metadata import resolve_metadata, Base, TvSeries


class Directory:
    """
    Class that encapsulates all of toktokkie's functionality
    """

    def __init__(self, path: str, generate_metadata: bool = False,
                 metadata_type: any = None):
        """
        Initializes the metadata of the directory
        :param path: The directory's path
        """
        self.path = path
        self.meta_dir = os.path.join(path, ".meta")
        self.icon_path = os.path.join(self.meta_dir, "icons")
        self.metadata_file = os.path.join(self.meta_dir, "info.json")

        if generate_metadata:
            if metadata_type is None:
                raise ValueError("Metadata type must be specified")
            self.generate_metadata(metadata_type)

        self.metadata = resolve_metadata(self.metadata_file)

    def generate_metadata(self, metadata_type: Base):
        """
        Prompts the user for metadata information
        :param metadata_type: The metadata type to generate
        :return: None
        """

        if os.path.isfile(self.metadata_file):
            prompt = input("Metadata File already exists. "
                           "Continuing will delete the previous data. "
                           "Continue? (y/n)")
            if prompt != "y":
                print("Aborting")
                sys.exit(0)

        metadata = metadata_type.generate_from_prompts(self.path)  # type: Base

        if not os.path.isdir(self.meta_dir):
            os.makedirs(self.meta_dir)
        metadata.write(self.metadata_file)

    def rename(self, scheme, agent, noconfirm: bool = False):
        """
        Renames the contained files according to a naming scheme.
        If the metadata type does not support renaming, this does nothing
        :param scheme: The naming scheme to use
        :param agent: The data gathering agent to use
        :param noconfirm: Skips the confirmation phase
        :return: None
        """
        if self.metadata.is_subclass_of(TvSeries):
            # noinspection PyTypeChecker
            renamer = Renamer(self.path, self.metadata, scheme, agent)
            renamer.rename(noconfirm)

    def iconize(self, method=None):
        """
        Applies the directory's icons
        :param method: The iconizing method to use
        :return: None
        """
        pass  # TODO iconize
