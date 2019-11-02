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













