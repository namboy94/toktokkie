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
from typing import Dict, Tuple, TYPE_CHECKING
from mutagen.easyid3 import EasyID3
# noinspection PyProtectedMember
from mutagen.id3._util import ID3NoHeaderError
from puffotter.os import get_ext
if TYPE_CHECKING:  # pragma: no cover
    from toktokkie.metadata.music.components.MusicAlbum import MusicAlbum


class MusicSong:
    """
    Class that models a single song
    """

    def __init__(self, path: str, album: "MusicAlbum"):
        """
        Initializes the object
        :param path: The path to the song file
        :param album: The album this song is a part of
        """

        self.logger = logging.getLogger(self.__class__.__name__)

        self.album = album
        self.path = path
        self.filename = str(os.path.basename(self.path))

        self.format = get_ext(self.path)

        tags = {}  # type: Dict[str, str]
        if self.format == "mp3":
            tags = self.__load_mp3_tags()
        self._tags = tags

    def save_tags(self):
        """
        Saves any edited tags
        :return: None
        """
        if self.format == "mp3":
            self.__write_mp3_tags()
        else:
            self.logger.warning("Can't write tags for {}: "
                                "not a known file type".format(self.path))

    def __load_mp3_tags(self) -> Dict[str, str]:
        """
        Loads MP3 tags if this is an mp3 file
        :return: The mp3 tags as a dictionary
        """
        try:
            tags = dict(EasyID3(self.path))

            for key in tags:
                tag = tags[key]
                if isinstance(tag, list):
                    if len(tag) >= 1:
                        tags[key] = tag[0]
                    else:
                        tags[key] = ""
            return tags

        except ID3NoHeaderError:
            return {}

    def __write_mp3_tags(self):
        """
        Writes the current tags to the file as ID3 tags, if this is an mp3 file
        :return: None
        """
        mp3 = EasyID3(self.path)
        for key, tag in self._tags.items():
            if tag == "":
                if key in mp3:
                    mp3.pop(key)
            else:
                mp3[key] = tag
        mp3.save()

    @property
    def title(self) -> str:
        """
        :return: The title of the song
        """
        title = self._tags.get("title")
        if title is not None:
            return title
        else:
            if self.filename.split(" - ")[0].isnumeric():
                return self.filename.split(" - ", 1)[1].rsplit(".", 1)[0]
            else:
                return self.filename.rsplit(".", 1)[0]

    @title.setter
    def title(self, title: str):
        """
        :param title: The title of the song
        :return: None
        """
        self._tags["title"] = title

    @property
    def artist_name(self) -> str:
        """
        :return: The song's artist name
        """
        return self._tags.get("artist", self.album.artist_name)

    @artist_name.setter
    def artist_name(self, name: str):
        """
        :param name: The song's artist name
        :return: None
        """
        self._tags["artist"] = name

    @property
    def album_artist_name(self) -> str:
        """
        :return: The song's album artist name
        """
        return self._tags.get("albumartist", self.album.artist_name)

    @album_artist_name.setter
    def album_artist_name(self, name: str):
        """
        :param name: The song's album artist name
        :return: None
        """
        self._tags["albumartist"] = name

    @property
    def album_name(self) -> str:
        """
        :return: The song's album name
        """
        return self._tags.get("album", self.album.name)

    @album_name.setter
    def album_name(self, name: str):
        """
        :param name: The song's album name
        :return: None
        """
        self._tags["album"] = name

    @property
    def genre(self) -> str:
        """
        :return: The song's genre
        """
        return self._tags.get("genre", self.album.genre)

    @genre.setter
    def genre(self, genre: str):
        """
        :param genre: The song's genre
        :return: None
        """
        self._tags["genre"] = genre

    @property
    def tracknumber(self) -> Tuple[int, int]:
        """
        :return: The song's track number as a tuple consisting of the song's
                 track number and the total amount of tracks in the album
        """
        tracks = [x.path for x in self.album.load_songs(False)]
        track_count = len(tracks)
        tracknumber = self._tags.get("tracknumber")

        if tracknumber is not None:
            split = tracknumber.split("/")
            if len(split) == 1:
                return int(tracknumber), track_count
            else:
                return int(split[0]), int(split[1])
        else:
            for i, track_path in enumerate(tracks):
                if track_path == self.path:
                    return i + 1, track_count
            return 1, track_count

    @tracknumber.setter
    def tracknumber(self, track_number: Tuple[int, int]):
        """
        :param track_number: The song's track number as a tuple consisting of
                             the song's track number and the total amount
                             of tracks in the album
        :return: None
        """
        track, total = track_number
        self._tags["tracknumber"] = "{}/{}".format(track, total)

    @property
    def year(self) -> int:
        """
        :return: The year this song was released
        """
        return int(self._tags.get("date", self.album.year))

    @year.setter
    def year(self, year: int):
        """
        :param year: The year this song was released
        :return: None
        """
        self._tags["date"] = str(year)
