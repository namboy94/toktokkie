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
from abc import ABC
from puffotter.os import listdir
from typing import Optional, Dict, List
from toktokkie.metadata.base.MetadataBase import MetadataBase


class GameExtras(MetadataBase, ABC):
    """
    Additional methods and attributes for game metadata objects
    """

    @property
    def video_dir(self) -> str:
        """
        :return: Path to the video directory
        """
        return os.path.join(self.directory_path, ".meta/videos")

    @property
    def cg_dir(self) -> str:
        """
        :return: Path to the CG directory
        """
        return os.path.join(self.directory_path, ".meta/cgs")

    @property
    def ost_dir(self) -> str:
        """
        :return: Path to the OST directory
        """
        return os.path.join(self.directory_path, ".meta/ost")

    @property
    def has_ed(self) -> bool:
        """
        :return: Whether or not the Visual Novel has an ending theme
        """
        return len(self.eds) > 0

    @property
    def has_op(self) -> bool:
        """
        :return: Whether or not the Visual Novel has an opening theme
        """
        return len(self.ops) > 0

    @property
    def has_cgs(self) -> bool:
        """
        :return: Whether or not the Visual Novel has a CG gallery
        """
        return len(self.cgs) > 0

    @property
    def has_ost(self) -> bool:
        """
        :return: Whether or not the Visual Novel has an OST
        """
        return len(self.ost) > 0

    @property
    def cgs(self) -> Dict[str, List[str]]:
        """
        Generates a dictionary of paths to CG images
        :return: A dictionary mapping the various CG images to their
                 respective directory identifiers
        """
        if not os.path.isdir(self.cg_dir):
            return {}
        else:
            cgs = {}
            for cg_dir, cg_dir_path in listdir(self.cg_dir, no_files=True):
                cgs[cg_dir] = []
                for _, img_path in listdir(cg_dir_path, no_dirs=True):
                    cgs[cg_dir].append(img_path)
            return cgs

    @property
    def ost(self) -> List[str]:
        """
        :return: a list of files for the OST of a visual novel
        """
        return self._get_file_list(self.ost_dir)

    @property
    def eds(self) -> List[str]:
        """
        :return: a list of ending theme videos
        """
        return self._get_file_list(self.video_dir, "ED")

    @property
    def ops(self) -> List[str]:
        """
        :return: a list of opening theme videos
        """
        return self._get_file_list(self.video_dir, "OP")

    @staticmethod
    def _get_file_list(path: str, prefix: Optional[str] = None) -> List[str]:
        """
        Retrieves a list of files from a directory
        :param path: The path to check
        :param prefix: An optional prefix
        :return: The list of files
        """
        if not os.path.isdir(path):
            return []
        else:
            files = []
            for _file, file_path in listdir(path, no_dirs=True):
                if prefix is not None and not _file.startswith(prefix):
                    continue
                files.append(file_path)
            return files
