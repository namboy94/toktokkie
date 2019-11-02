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

import json
from flask import redirect, url_for
from toktokkie.web import app, db
from toktokkie.Directory import Directory
from toktokkie.web.models.MediaLocation import MediaLocation
from toktokkie.web.models.CachedDirectory import CachedDirectory


@app.route("/update", methods=["GET"])
def update():
    """
    Updates the cache
    :return: A redirect to the index page
    """

    for x in CachedDirectory.query.all():
        db.session.delete(x)

    paths = [x.path for x in MediaLocation.query.all()]

    for path in paths:
        directories = Directory.load_child_directories(path)
        for _directory in directories:
            cached = CachedDirectory(
                path=_directory.path,
                metadata_json=json.dumps(_directory.metadata.json)
            )
            db.session.add(cached)
    db.session.commit()

    redirect(url_for("index"))
