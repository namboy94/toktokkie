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
import logging
import mimetypes
from typing import Dict, Any, List
from puffotter.os import listdir
from toktokkie.enums import IdType
from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.base.IdHelper import IdHelper
from toktokkie.metadata.base.components.JsonComponent import JsonComponent
from toktokkie.metadata.music.components.MusicSong import MusicSong
from toktokkie.metadata.music.components.MusicVideo import MusicVideo


class MusicAlbum(JsonComponent):
    """
    Class that defines attributes of music albums
    """

    def __init__(
            self,
            parent_path: str,
            parent_ids: Dict[IdType, List[str]],
            ids: Dict[IdType, List[str]],
            name: str,
            genre: str,
            year: int
    ):
        """
        Initializes the MusicAlbum object
        :param parent_path: The path to the parent directory
        :param parent_ids: The IDs associated with the parent
        :param ids: The specific IDs for this album
        :param name: The name of the album
        :param genre: The genre of the album
        :param year: The year this album was released
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.parent_path = parent_path
        self.parent_ids = parent_ids

        self.artist_name = os.path.basename(os.path.abspath(parent_path))

        self.name = name
        self.genre = genre
        self.year = year
        self.path = os.path.join(parent_path, self.name)

        self.ids = IdHelper.fill_ids(
            ids, [IdType.MUSICBRAINZ_RELEASE], parent_ids
        )

    @property
    def json(self) -> Dict[str, Any]:
        """
        Converts the component into a JSON-compatible dictionary
        :return: The JSON-compatible dictionary
        """
        return {
            "name": self.name,
            "genre": self.genre,
            "year": self.year,
            "ids": IdHelper.stringify_ids(
                IdHelper.minimize_ids(self.ids, self.parent_ids)
            )
        }

    @classmethod
    def from_json(
            cls,
            parent_path: str,
            parent_ids: Dict[IdType, List[str]],
            json_data: Dict[str, Any]
    ) -> "MusicAlbum":
        """
        Generates a new MusicAlbum object based on JSON data
        :param parent_path: The path to the parent metadata directory
        :param parent_ids: The IDs of the parent metadata
        :param json_data: The JSON data
        :return: The generated object
        :raises InvalidMetadataException: If the provided JSON is invalid
        """
        try:
            return cls(
                parent_path,
                parent_ids,
                IdHelper.objectify_ids(json_data["ids"]),
                json_data["name"],
                json_data["genre"],
                json_data["year"]
            )
        except KeyError as e:
            raise InvalidMetadata(f"Attribute missing: {e}")

    def load_songs(self, tracknumber_sort: bool = True) -> List["MusicSong"]:
        """
        Loads songs from this album
        :param tracknumber_sort: Whether or not to sort the songs by
                                 tracknumber
                                 Needed to avoid infinite recursion
                                 in MusicSong class
        :return: All songs in this album
        """
        song_files = self.__get_files("audio")
        songs = [MusicSong(x, self) for x in song_files]
        songs.sort(key=lambda x: x.path)
        if tracknumber_sort:
            songs.sort(key=lambda x: x.tracknumber[0])
        return songs

    @property
    def songs(self) -> List["MusicSong"]:
        """
        :return: All songs in this album
        """
        return self.load_songs(True)

    @property
    def videos(self) -> List["MusicVideo"]:
        """
        :return: All music videos in this album
        """
        video_files = self.__get_files("video")
        videos = [MusicVideo(x, self) for x in video_files]
        videos.sort(key=lambda x: x.title)
        return videos

    def __get_files(self, mimetype: str) -> List[str]:
        """
        Retrieves the files in the album directory based on their mime type
        :param mimetype: The mime type of the files to find
        :return: The files with that mimetype
        """
        files = []
        for _file, path in listdir(self.path, no_dirs=True):
            guess = str(mimetypes.MimeTypes().guess_type(path)[0])
            if guess.startswith(mimetype):
                files.append(path)
        return files
