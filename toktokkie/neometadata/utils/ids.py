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

from typing import Dict, List, Optional
from toktokkie.neometadata.enums import IdType, MediaType


def stringify_ids(ids: Dict[IdType, List[str]]) -> Dict[str, List[str]]:
    """
    Converts the keys in an ID dictionary to strings
    :param ids: The ID dictionary to convert
    :return: The converted ID dictionary
    """
    new_ids = {}
    for id_type, values in ids.items():
        new_ids[id_type.value] = values
    return new_ids


def objectify_ids(ids: Dict[str, List[str]]) -> Dict[IdType, List[str]]:
    """
    Converts the keys in an ID dictionary using string keys to IdType objects
    :param ids: The ID dictionary to convert
    :return: The converted ID dictionary
        """
    new_ids = {}
    for id_type, values in ids.items():
        new_ids[IdType(id_type)] = values
    return new_ids


def fill_ids(
        ids: Dict[IdType, List[str]],
        valid_ids: List[IdType],
        _parent_ids: Optional[Dict[IdType, List[str]]] = None
) -> Dict[IdType, List[str]]:
    """
    Fills in any missing id type key for an ID dictionary
    :param ids: The ID dictionary to fill
    :param valid_ids: Any valid ID types
    :param _parent_ids: Optionally provided dictionary of parent IDs.
                        The values of this dictionary will be entered into the
                        filled dictionary if they aren't defined already
    :return: The filled dictionary
    """
    parent_ids = {} if _parent_ids is None else _parent_ids
    for id_type, values in parent_ids.items():
        if id_type not in ids:
            ids[id_type] = values

    for id_type in valid_ids:
        if id_type not in ids:
            ids[id_type] = []
    return ids


def minimize_ids(
        ids: Dict[IdType, List[str]],
        _parent_ids: Optional[Dict[IdType, List[str]]] = None
) -> Dict[IdType, List[str]]:
    """
    Removes redundant and empty IDs from a dictionary of IDs
    :param ids: The dictionary to minimize
    :param _parent_ids: Optionally provide a parent's IDs. These IDs will
                        be removed from the child dictionary if the values
                        are the same
    :return: The minimized dictionary
    """
    parent_ids = {} if _parent_ids is None else _parent_ids
    minimized = {}

    for id_type in ids.keys():
        values = ids[id_type]

        if values == parent_ids.get(id_type):
            continue

        if len(ids[id_type]) > 0:
            minimized[id_type] = values

    return minimized


literature_media_types = [
    MediaType.BOOK,
    MediaType.BOOK_SERIES,
    MediaType.COMIC
]
"""
Media types that represent literature
"""


int_id_types = [
    IdType.MYANIMELIST,
    IdType.ANILIST,
    IdType.KITSU,
    IdType.TVDB
]
"""
ID Types that are always integer values
"""


theme_song_ids = [
    IdType.TVDB,
    IdType.MYANIMELIST,
    IdType.ANILIST,
    IdType.KITSU,
    IdType.VNDB,
    IdType.MUSICBRAINZ_RECORDING
]
"""
ID types that can be associated with theme songs
"""


urlmap = {
    IdType.ANILIST: "https://anilist.co/@{ANIME_MANGA}/{}",
    IdType.MYANIMELIST: "https://myanimelist.net/@{ANIME_MANGA}/{}",
    IdType.KITSU: "https://kitsu.io/@{ANIME_MANGA}/{}",
    IdType.TVDB: "https://www.thetvdb.com/?id={}&tab=series",
    IdType.VNDB: "https://vndb.org/{}",
    IdType.IMDB: "https://www.imdb.com/title/{}",
    IdType.ISBN: "https://isbnsearch.org/isbn/{}",
    IdType.MANGADEX: "https://mangadex.org/title/{}",
    IdType.MUSICBRAINZ_ARTIST: "https://musicbrainz.org/artist/{}",
    IdType.MUSICBRAINZ_RECORDING: "https://musicbrainz.org/recording/{}",
    IdType.MUSICBRAINZ_RELEASE: "https://musicbrainz.org/release/{}"
}
"""
Maps ID types to URL schemas
"""
