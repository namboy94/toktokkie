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
from flask import render_template, request, redirect, url_for
from toktokkie.web import app, db
from toktokkie.web.models.MediaLocation import MediaLocation


@app.route("/configure")
def configure():
    """
    Shows the configuration page
    :return: The configuration page
    """
    paths = [x.path for x in MediaLocation.query.all()]
    return render_template("configure.html", paths=paths)


@app.route("/delete_content_dir", methods=["POST"])
def delete_content_dir():
    """
    Deletes a content directory
    :return: A redirect to the configuration page
    """
    target = request.form.get("target")
    if target is not None:
        location = MediaLocation.query.filter_by(path=target).first()
        db.session.delete(location)
        db.session.commit()
    return redirect(url_for("configure"))


@app.route("/add_content_dir", methods=["POST"])
def add_content_dir():
    """
    Adds a content directory
    :return: A redirect to the configuration page
    """
    target = os.path.abspath(request.form.get("target"))
    if target is not None and os.path.isdir(target):
        location = MediaLocation(path=target)
        db.session.add(location)
        db.session.commit()
    return redirect(url_for("configure"))
