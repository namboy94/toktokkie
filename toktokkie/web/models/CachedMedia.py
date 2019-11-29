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

from toktokkie.web import db


class CachedMedia(db.Model):
    """
    Database table that stores a cached version of a media file
    """

    __tablename__ = "cached_media"
    """
    The table name
    """

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    """
    The ID of the cached media
    """

    path = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    """
    The path to the cached media file
    """

    data = db.Column(db.BLOB, nullable=False)
    """
    The media data
    """

    format = db.Column(db.String(255), nullable=False)
    """
    The media format
    """

    media_type = db.Column(db.String(255), nullable=False)
    """
    The type of media (video, image etc)
    """

    @property
    def mimetype(self) -> str:
        """
        :return: The media mimetype
        """
        return self.media_type + "/" + self.format
