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
from flask import render_template, Response, request, redirect, url_for
from puffotter.os import get_ext
from toktokkie.web import app, db
from toktokkie.Directory import Directory
from toktokkie.web.models.MediaLocation import MediaLocation
from toktokkie.web.models.CachedDirectory import CachedDirectory
from toktokkie.metadata.MediaType import MediaType
from toktokkie.metadata.functions import get_metadata_class


@app.route("/")
def index():
    """
    List all directories that were found in the stored content directories
    :return: The response
    """

    mapped_dirs = {x: [] for x in MediaType}
    cached_dirs = CachedDirectory.query.all()

    for cached in cached_dirs:
        cached_data = json.loads(cached.metadata_json)
        metadata = get_metadata_class(cached_data["type"])(
            directory_path=cached.path,
            json_data=cached_data,
            no_validation=True
        )
        _directory = Directory(cached.path, metadata=metadata)
        mapped_dirs[_directory.metadata.media_type()].append(_directory)

    media_names = sorted([x for x in MediaType], key=lambda x: x.value)
    media_dirs = []

    for media_type in media_names:
        media_dirs.append((media_type, mapped_dirs[media_type]))

    return render_template("index.html", media_dirs=media_dirs)


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


@app.route("/content_dirs", methods=["GET"])
def content_dirs():
    paths = [x.path for x in MediaLocation.query.all()]
    return render_template("content_dirs.html", paths=paths)


@app.route("/delete_content_dir", methods=["POST"])
def delete_content_dir():
    target = request.form.get("target")
    if target is not None:
        location = MediaLocation.query.filter_by(path=target).first()
        db.session.delete(location)
        db.session.commit()
    return redirect(url_for("content_dirs"))


@app.route("/add_content_dir", methods=["POST"])
def add_content_dir():
    target = os.path.abspath(request.form.get("target"))
    if target is not None and os.path.isdir(target):
        location = MediaLocation(path=target)
        db.session.add(location)
        db.session.commit()
    return redirect(url_for("content_dirs"))


@app.route("/directory", methods=["GET"])
def directory():
    path = request.args.get("path")
    _directory = Directory(path)
    return render_template("directory.html", directory=_directory)


@app.route("/update", methods=["GET"])
def update():

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

    redirect(url_for("/"))
