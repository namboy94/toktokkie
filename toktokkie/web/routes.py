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
from typing import List, Dict
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
    return redirect(url_for("listings", category_method="media_type"))


@app.route("/listings/<category_method>")
def listings(category_method: str):

    directory_data = {}  # type: Dict[str, List[Directory]]
    cached_dirs = CachedDirectory.query.all()
    directory_objs = [x.load_directory() for x in cached_dirs]

    if category_method == "media_type":

        def fancy_media_type(string) -> str:
            strings = string.replace("_", " ").split(" ")
            string = " ".join([x[0].upper() + x[1:] for x in strings])
            return string

        directory_data = {fancy_media_type(x.value): [] for x in MediaType}

        for directory_obj in directory_objs:
            media_type = fancy_media_type(
                directory_obj.metadata.media_type().value
            )
            directory_data[media_type].append(directory_obj)

    elif category_method == "tags":

        for directory_obj in directory_objs:
            for tag in directory_obj.metadata.tags:
                if tag not in directory_data:
                    directory_data[tag] = [directory_obj]
                else:
                    directory_data[tag].append(directory_obj)

    elif category_method == "parent":

        for directory_obj in directory_objs:
            parent = os.path.dirname(directory_obj.path)
            if parent not in directory_data:
                directory_data[parent] = [directory_obj]
            else:
                directory_data[parent].append(directory_obj)

    sorted_directory_data = []
    for key in sorted(directory_data.keys()):
        directories = directory_data[key]
        directories.sort(key=lambda x: x.metadata.name)
        sorted_directory_data.append((key, directories))

    return render_template(
        "listings.html",
        directory_data=sorted_directory_data
    )


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
