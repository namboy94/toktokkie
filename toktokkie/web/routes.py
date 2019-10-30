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
import shutil
from toktokkie.web import app
from flask import render_template, Response, request
from toktokkie.Directory import Directory


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/image")
def image():
    path = request.args["path"]
    with open(path, "rb") as f:
        return Response(f.read(), mimetype="image/png")


@app.route("/list")
def list_dirs():
    media_paths = [
        "/home/hermann/Downloads/test"
    ]
    media_dirs = []
    for path in media_paths:
        media_dirs += Directory.load_directories(path)

    return render_template("list.html", media_dirs=media_dirs)
