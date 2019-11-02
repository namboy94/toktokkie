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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from puffotter.os import makedirs

root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(os.path.expanduser("~"), ".config/toktokkie")
sqlite_uri = "sqlite:///" + os.path.join(config_path, "web.models")
makedirs(config_path)

app = Flask("toktokkie", root_path=root_path)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# noinspection PyUnresolvedReferences
def init_db():
    """
    Initializes the database
    :return: None
    """
    with app.app_context():
        from toktokkie.web.models.MediaLocation import MediaLocation
        from toktokkie.web.models.CachedDirectory import CachedDirectory
        db.create_all()


# noinspection PyUnresolvedReferences
def init_routes():
    """
    Initializes the app routes
    :return:
    """
    import toktokkie.web.routes.directories
    import toktokkie.web.routes.update
    import toktokkie.web.routes.config
    import toktokkie.web.routes.listings
    import toktokkie.web.routes.media
    import toktokkie.web.routes.root
