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
import json
from typing import Union, Type
from toktokkie.neometadata.base.Metadata import Metadata
from toktokkie.neometadata.tv.Tv import Tv
from toktokkie.neometadata.book.Book import Book
from toktokkie.neometadata.book_series.BookSeries import BookSeries
from toktokkie.neometadata.comic.Comic import Comic
from toktokkie.neometadata.music.Music import Music
from toktokkie.neometadata.movie.Movie import Movie
from toktokkie.neometadata.enums import MediaType
from toktokkie.exceptions import InvalidMetadata


def get_metadata(directory: str) -> Metadata:
    """
    Automatically resolves the metadata of a directory
    :param directory: The directory for which to generate the metadata
    :return: The generated metadata
    :raises InvalidMetadataException: If the metadata is invalid
    """
    info_file = os.path.join(directory, ".meta/info.json")
    try:
        with open(info_file, "r") as f:
            media_type = json.load(f)["type"]
            metadata_cls = get_metadata_class(media_type)
            return metadata_cls(directory)
    except (KeyError, ValueError) as e:
        raise InvalidMetadata(f"Missing/Invalid attribute: {e}")


def create_metadata(directory: str, media_type: Union[str, MediaType]) \
        -> Metadata:
    """
    Generates a new metadata object using user prompts
    :param directory: The directory for which to generate the metadata
    :param media_type: The media type of the metadata
    :return: The generated metadata
    """
    metadata_cls = get_metadata_class(media_type)
    metadata = metadata_cls.from_prompt(directory)
    metadata.write()
    return metadata


def get_metadata_class(media_type: Union[str, MediaType]) -> Type[Metadata]:
    """
    Retrieves the metadata class for a given media type
    :param media_type: The media type for which to get the metadata class
    :return: The metadata class
    """
    if type(media_type) == str:
        media_type = MediaType(media_type)

    mapping = {
        x.media_type(): x
        for x in [
            Tv
        ]
    }
    return mapping[media_type]
