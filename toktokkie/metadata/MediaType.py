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
from enum import Enum


class MediaType(Enum):
    """
    Enumeration that defines all possible media types
    """
    BOOK = "book"
    BOOK_SERIES = "book_series"
    MOVIE = "movie"
    TV_SERIES = "tv"
    VISUAL_NOVEL = "visual_novel"
    MANGA = "manga"
    MUSIC_ARTIST = "music"
