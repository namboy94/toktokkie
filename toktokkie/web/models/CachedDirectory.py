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
from toktokkie.web import db
from toktokkie.Directory import Directory
from toktokkie.metadata.functions import get_metadata_class


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

    def load_directory(self) -> Directory:
        json_data = json.loads(self.metadata_json)
        metadata = get_metadata_class(json_data["type"])(
            self.path,
            json_data=json_data,
            no_validation=True
        )
        return Directory(self.path, metadata=metadata)
