#!/bin/env python
"""LICENSE
Copyright 2019 Hermann Krumrey <hermann@krumreyh.com>

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
along with toktokkie-gui.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
from subprocess import check_output

qt_designer_dir = os.path.join("toktokkie", "gui", "qt_designer")
pyuic_dir = os.path.join("toktokkie", "gui", "pyuic")

for design in os.listdir(qt_designer_dir):

    if design.endswith(".ui"):

        design_file = os.path.join(qt_designer_dir, design)
        result_file = os.path.join(pyuic_dir, design.replace(".ui", ".py"))
        generated = check_output(["pyuic5", design_file])
        with open(result_file, "wb") as f:
            f.write(generated)
