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
from typing import List, Dict
from flask import render_template
from toktokkie.web import app
from toktokkie.web.models.CachedDirectory import CachedDirectory
from toktokkie.metadata.MediaType import MediaType


@app.route("/listings/<category_method>")
def listings(category_method: str):
    """
    Lists all cached directories
    :param category_method: Specifies by what metric to categorize the
                            directories.
    :return: The generated HTML
    """
    display_data = {}  # type: Dict[str, List[CachedDirectory]]
    cached_dirs = CachedDirectory.query.all()

    if category_method == "media_type":

        def fancy_media_type(string) -> str:
            strings = string.replace("_", " ").split(" ")
            string = " ".join([x[0].upper() + x[1:] for x in strings])
            return string

        display_data = {fancy_media_type(x.value): [] for x in MediaType}

        for cached_dir in cached_dirs:
            media_type = fancy_media_type(
                cached_dir.directory.metadata.media_type().value
            )
            display_data[media_type].append(cached_dir)

    elif category_method == "tags":

        for cached_dir in cached_dirs:
            for tag in cached_dir.directory.metadata.tags:
                if tag not in display_data:
                    display_data[tag] = [cached_dir]
                else:
                    display_data[tag].append(cached_dir)

    elif category_method == "parent":

        for cached_dir in cached_dirs:
            parent = os.path.dirname(cached_dir.path)
            if parent not in display_data:
                display_data[parent] = [cached_dir]
            else:
                display_data[parent].append(cached_dir)

    sorted_directory_data = []
    for key in sorted(display_data.keys()):
        directories = display_data[key]
        directories.sort(key=lambda x: x.directory.metadata.name)
        sorted_directory_data.append((key, directories))

    return render_template(
        "listings.html",
        directory_data=sorted_directory_data
    )
