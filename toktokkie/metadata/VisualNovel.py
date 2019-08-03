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
from typing import Optional, List, Dict
from puffotter.os import listdir
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.helper.wrappers import json_parameter
from toktokkie.metadata.components.enums import VisualNovelIdType, MediaType


class VisualNovel(Metadata):
    """
    Metadata class that model a visual novel
    """

    @classmethod
    def id_type(cls) -> type(VisualNovelIdType):
        """
        :return: The ID type used by this metadata object
        """
        return VisualNovelIdType

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        return MediaType.VISUAL_NOVEL

    @classmethod
    def prompt(cls, directory_path: str) -> Metadata:
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        print("Generating metadata for {}:"
              .format(os.path.basename(directory_path)))
        return cls(directory_path, {
            "ids": cls.prompt_for_ids(required=[VisualNovelIdType.VNDB]),
            "type": cls.media_type().value
        })

    @property
    @json_parameter
    def has_ed(self) -> bool:
        """
        :return: Whether or not the Visual Novel has an ending theme
        """
        return self.json.get("has_ed", True)

    @has_ed.setter
    def has_ed(self, has_ed: bool):
        """
        Setter method for the has_ed property
        :param has_ed: Whether or not the VN has an ending theme
        :return: None
        """
        self.json["has_ed"] = has_ed

    @property
    @json_parameter
    def has_op(self) -> bool:
        """
        :return: Whether or not the Visual Novel has an opening theme
        """
        return self.json.get("has_ed", True)

    @has_op.setter
    def has_op(self, has_ed: bool):
        """
        Setter method for the has_op property
        :param has_ed: Whether or not the VN has an opening theme
        :return: None
        """
        self.json["has_ed"] = has_ed

    @property
    def cgs(self) -> Optional[Dict[str, str]]:
        """
        Generates a dictionary of paths to CG images
        :return: A dictionary mapping the various CG images to their
                 respective directory identifiers
        """

        cg_dirs = os.path.join(self.directory_path, ".meta/cgs")
        if not os.path.isdir(cg_dirs):
            return None
        else:
            cgs = {}
            for cg_dir, cg_dir_path in listdir(cg_dirs, no_files=True):
                for _, img_path in listdir(cg_dir_path, no_dirs=True):
                    cgs[cg_dir] = img_path
            return cgs

    @property
    def ost(self) -> Optional[List[str]]:
        """
        :return: a list of files for the OST of a visual novel
        """
        ost_dir = os.path.join(self.directory_path, ".meta/ost")
        if not os.path.isdir(ost_dir):
            return None
        else:
            ost = []
            for _, music_file in listdir(ost_dir, no_dirs=True):
                ost.append(music_file)
            return ost

    @property
    def ed(self) -> Optional[List[str]]:
        """
        :return: a list of ending theme videos
        """
        video_dir = os.path.join(self.directory_path, ".meta/videos")
        if not os.path.isdir(video_dir):
            return None
        else:
            eds = []
            for video, video_path in listdir(video_dir, no_dirs=True):
                if video.startswith("ED"):
                    eds.append(video_path)
            return eds

    @property
    def op(self) -> Optional[List[str]]:
        """
        :return: a list of opening theme videos
        """
        video_dir = os.path.join(self.directory_path, ".meta/videos")
        if not os.path.isdir(video_dir):
            return None
        else:
            ops = []
            for video, video_path in listdir(video_dir, no_dirs=True):
                if video.startswith("OP"):
                    ops.append(video_path)
            return ops
