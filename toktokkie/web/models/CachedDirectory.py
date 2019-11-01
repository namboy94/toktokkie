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
from toktokkie.web import db


class CachedDirectory(db.Model):
    """
    Database table that stores a cached version of a media Directory
    """

    __tablename__ = "cached_directories"
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
    The ID of the cached directory
    """

    path = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    """
    The path to the cached directory
    """

    metadata_json = db.Column(
        db.String(),
        nullable=False
    )

    @property
    def name(self) -> str:
        return os.path.basename(os.path.abspath(self.path))
