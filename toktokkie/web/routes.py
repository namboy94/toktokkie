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
from flask import render_template, Response, request
from puffotter.os import get_ext
from toktokkie.web import app
from toktokkie.Directory import Directory
from toktokkie.web.models.MediaLocation import MediaLocation


@app.route("/")
def root():
    paths = [x.path for x in MediaLocation.query.all()]

    media_dirs = []
    for path in paths:
        media_dirs += Directory.load_directories(path)

    return render_template("list.html", media_dirs=media_dirs)


@app.route("/image/<image_format>")
def image(image_format: str) -> Response:
    """
    Sends an image file from the local file system
    :return: A PNG image read from a local file
    """
    path = request.args.get("path")
    ext = get_ext(path)

    if path is None or not os.path.isfile(path) or ext != image_format:
        return Response(status=404)
    else:
        with open(path, "rb") as f:
            return Response(f.read(), mimetype="image/" + image_format)
