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

from typing import Dict, Any
from toktokkie.metadata.types.components.MusicAlbum import MusicAlbum
from toktokkie.metadata.types.components.Component import Component
from toktokkie.metadata.ids.mappings import theme_song_ids
from toktokkie.metadata.ids.functions import objectify_ids, stringify_ids, \
    fill_ids, minimize_ids


class MusicThemeSong(Component):

    def __init__(
            self,
            album: MusicAlbum,
            json_data: Dict[str, Any]
    ):
        self.album = album
        self.name = json_data["name"]
        self.theme_type = json_data["theme_type"]

        if self.name != self.album.name:
            self.logger.warning("Theme song {} does not match album {}"
                                .format(self.name, self.album.name))

        ids = objectify_ids(json_data.get("series_ids"))  # type: ignore
        self.series_ids = fill_ids(ids, theme_song_ids)

    @property
    def json(self) -> Dict[str, Any]:
        """
        Converts the component into a JSON-compatible dictionary
        :return: The JSON-compatible dictionary
        """
        return {
            "name": self.name,
            "series_ids": stringify_ids(minimize_ids(self.series_ids))
        }
