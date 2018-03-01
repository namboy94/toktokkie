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


class Scheme:

    scheme_name = "scheme"

    illegal_characters = {
        "/": " ",
        "\\": " ",
        "?": " ",
        "<": " ",
        ">": " ",
        ":": " - ",
        "*": " ",
        "|": " ",
        "\"": " ",
        "^": " "
    }

    @classmethod
    def sanitize(cls, string: str) -> str:
        sanitized = string
        for illegal_character, replacement in cls.illegal_characters.items():
            sanitized = sanitized.replace(illegal_character, replacement)
        return sanitized

    @classmethod
    def generate_episode_name(cls, series_name: str, season: int,
                              episode: int, episode_name: str) -> str:
        return cls.sanitize(
            cls.format_episode_name(series_name, season, episode, episode_name)
        )

    @classmethod
    def _format_episode_name(cls, series_name: str, season: int,
                            episode: int, episode_name: str) -> str:
        raise NotImplementedError()
