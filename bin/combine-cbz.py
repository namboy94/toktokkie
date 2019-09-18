#!/usr/bin/env python

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
import argparse
from subprocess import Popen
from puffotter.os import listdir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--delete-original", action="store_true")
    args = parser.parse_args()

    fill = len(str(len(args.files)))

    dest_dir = args.files[0] + "_combined_dir"
    dest_file = args.files[0] + "_combined.cbz"
    src_images = []

    if os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    for i, cbz in enumerate(args.files):

        tempdir = "combine_temp"
        if os.path.isdir(tempdir):
            shutil.rmtree(tempdir)

        Popen(["unzip", cbz, "-d", tempdir]).wait()

        for name, path in listdir(tempdir):
            new_name = str(i).zfill(fill) + " - " + name
            new_path = os.path.join(dest_dir, new_name)
            src_images.append(new_path)
            os.rename(path, new_path)

        shutil.rmtree(tempdir)
        if args.delete_original:
            os.remove(cbz)

    Popen(["zip", "-j", dest_file] + src_images).wait()
    shutil.rmtree(dest_dir)


if __name__ == "__main__":
    main()
