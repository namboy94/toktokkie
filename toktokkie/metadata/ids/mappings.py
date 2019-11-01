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

from typing import List, Dict
from toktokkie.metadata.MediaType import MediaType
from toktokkie.metadata.ids.IdType import IdType


valid_id_types = {
    MediaType.BOOK: [
        IdType.ISBN,
        IdType.ANILIST,
        IdType.MYANIMELIST,
        IdType.KITSU
    ],
    MediaType.BOOK_SERIES: [
        IdType.ISBN,
        IdType.ANILIST,
        IdType.MYANIMELIST,
        IdType.KITSU
    ],
    MediaType.MOVIE: [
        IdType.IMDB,
        IdType.ANILIST,
        IdType.MYANIMELIST,
        IdType.KITSU
    ],
    MediaType.TV_SERIES: [
        IdType.TVDB,
        IdType.ANILIST,
        IdType.MYANIMELIST,
        IdType.KITSU
    ],
    MediaType.VISUAL_NOVEL: [
        IdType.VNDB
    ],
    MediaType.MANGA: [
        IdType.ISBN,
        IdType.ANILIST,
        IdType.MYANIMELIST,
        IdType.KITSU,
        IdType.MANGADEX
    ],
    MediaType.MUSIC_ARTIST: [
        IdType.MUSICBRAINZ_ARTIST
    ]
}  # type: Dict[MediaType, List[IdType]]
"""
Valid ID types for the various Media types
"""


required_id_types = {
    MediaType.BOOK: [
    ],
    MediaType.BOOK_SERIES: [
    ],
    MediaType.MOVIE: [
        IdType.IMDB
    ],
    MediaType.TV_SERIES: [
        IdType.TVDB
    ],
    MediaType.VISUAL_NOVEL: [
        IdType.VNDB
    ],
    MediaType.MANGA: [
    ],
    MediaType.MUSIC_ARTIST: [
        IdType.MUSICBRAINZ_ARTIST
    ]
}  # type: Dict[MediaType, List[IdType]]
"""
Required ID Types for the various Media Types
"""


literature_media_types = [
    MediaType.BOOK,
    MediaType.BOOK_SERIES,
    MediaType.MANGA
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


id_prompt_order = [
    IdType.TVDB,
    IdType.IMDB,
    IdType.ISBN,
    IdType.VNDB,
    IdType.MUSICBRAINZ_ARTIST,
    IdType.MUSICBRAINZ_RELEASE,
    IdType.MUSICBRAINZ_RECORDING,
    IdType.MYANIMELIST,
    IdType.ANILIST,
    IdType.KITSU,
    IdType.MANGADEX
]
"""
The order in which ID types should be prompted
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
