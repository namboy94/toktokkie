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
from typing import Dict
from unittest import TestCase
from toktokkie.Directory import Directory
from toktokkie.verification.Verificator import Verificator


class TestVerificator(TestCase):
    """
    Test class for a verificator. Also defines common methods for all
    other verificator tests
    """

    verificator_cls = Verificator
    """
    The verificator class to test
    """

    testdir = "testdir"
    """
    Directory in which to store any generated files
    """

    structure = {}
    """
    The structure to generate during setup
    """

    metadatas = {}
    """
    Metadata information for directories
    """

    verificators = {}
    """
    A verificator for each directory
    """

    def setUp(self):
        """
        Creates the test directory after deleting any previously existing ones
        :return: None
        """
        self.cleanup()
        os.makedirs(self.testdir)
        self.generate_structure(self.structure)
        for directory, metadata in self.metadatas.items():
            metadata.write(os.path.join(
                self.testdir, directory, ".meta", "info.json"
            ))
            directory = Directory(os.path.join(self.testdir, directory))
            self.verificators[directory] = self.verificator_cls(directory)

    def tearDown(self):
        """
        Deletes all test directories
        :return: None
        """
        self.cleanup()

    def cleanup(self):
        """
        Cleans up files and directories generated while testing
        :return: None
        """
        if os.path.isdir(self.testdir):
            shutil.rmtree(self.testdir)

    def generate_structure(self,
                           structure: Dict[str, dict or list],
                           previous: str = None):
        """
        Generates a file system structure
        :param structure: The structure to generate
        :param previous: Used for recursive calls
        :return: None
        """

        if previous is None:
            previous = self.testdir

        for child in structure:
            child_path = os.path.join(previous, child)

            if not child.startswith(".") and "." in child or \
                    isinstance(structure, list):
                with open(child_path, "w") as f:
                    f.write("placeholder")

            elif isinstance(structure, dict):
                os.makedirs(child_path)
                self.generate_structure(structure[child], child_path)
