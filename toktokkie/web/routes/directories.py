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

from flask import render_template, request, Response
from toktokkie.web import app
from toktokkie.web.models.CachedDirectory import CachedDirectory


@app.route("/directory", methods=["GET"])
def directory():
    """
    Displays a single directory
    :return: The HTML for the directory page
    """
    path = request.args.get("path")
    cached = CachedDirectory.query.filter_by(path=path).first()
    if cached is None:
        return Response(404)
    else:
        return render_template(
            "directory.html",
            cached=cached,
            directory=cached.directory,
            metadata=cached.directory.metadata,
            icon=cached.icon_url,
            title=cached.directory.metadata.name
        )
