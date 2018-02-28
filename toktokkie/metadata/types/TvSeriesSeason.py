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


class TvSeriesSeason:
    """
    A TV Series Season that can easily be serialized into a dictionary
    """

    def __init__(self, name: str, season_data: dict):
        self.name = name
        self.tvdb_urls = season_data["tvdb_urls"]
        self.audio_langs = season_data["audio_langs"]
        self.subtitle_langs = season_data["subtitle_langs"]
        self.resolutions = []

        for resolution in season_data["resolutions"]:
            self.resolutions.append()

    def to_json(self) -> dict:
