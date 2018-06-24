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
from typing import Dict, List, Callable, Any, Tuple
from unittest import TestCase, mock
from toktokkie.Directory import Directory
from toktokkie.metadata.Base import Base
from toktokkie.metadata.TvSeries import TvSeries
from toktokkie.metadata.AnimeSeries import AnimeSeries
from toktokkie.metadata.Movie import Movie
from toktokkie.metadata.AnimeMovie import AnimeMovie
from toktokkie.verification.Verificator import Verificator


class TestVerificator(TestCase):
    """
    Test class for a verificator. Also defines common methods for all
    other verificator tests
    """

    testdir = "testdir"
    """
    Directory in which to store any generated files
    """

    verificator_cls = Verificator
    """
    The verificator class to test
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

            metadata_dir = os.path.join(self.testdir, directory, ".meta")
            if not os.path.isdir(metadata_dir):
                os.makedirs(metadata_dir)

            metadata.write(os.path.join(metadata_dir, "info.json"))
            toktokkie_dir = Directory(os.path.join(self.testdir, directory))
            self.verificators[directory] =\
                self.verificator_cls(toktokkie_dir, {})

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

            if (not child.startswith(".") and "." in child) or \
                    isinstance(structure, list):
                with open(child_path, "w") as f:
                    f.write("placeholder")

            elif isinstance(structure, dict):
                os.makedirs(child_path)
                self.generate_structure(structure[child], child_path)

    @staticmethod
    def execute_with_mocked_input(
            prompt_input: List[str], action: Callable
    ) -> Any:
        """
        Executes a function with mocked user input
        :param prompt_input: The user input to mock
        :param action: The function to execute
        :return: The return value of the function
        """
        with mock.patch("builtins.input", side_effect=prompt_input):
            return action()

    def generate_sample_metadata(self) \
            -> Tuple[Base, TvSeries, AnimeSeries, Movie, AnimeMovie]:
        """
        Generates some sample metadata files in the 'testdir' directory
        :return: A tuple of metadata directories
        """

        self.generate_structure({
            "a": [],
            "b": [],
            "c": [],
            "d": [],
            "e": []
        })

        base = self.execute_with_mocked_input(
            ["", "", ""],
            lambda: Directory(os.path.join(self.testdir, "a"), True, Base)
        )
        tv_series = self.execute_with_mocked_input(
            ["", "", "", "", ""],
            lambda: Directory(os.path.join(self.testdir, "b"), True, TvSeries)
        )
        anime_series = self.execute_with_mocked_input(
            ["", "", "", "", "", "", "", "", ""],
            lambda:
            Directory(os.path.join(self.testdir, "c"), True, AnimeSeries)
        )
        movie = self.execute_with_mocked_input(
            ["", "", "1", "", "", ""],
            lambda: Directory(os.path.join(self.testdir, "d"), True, Movie)
        )
        anime_movie = self.execute_with_mocked_input(
            ["", "", "1", "", "", "", "1"],
            lambda:
            Directory(os.path.join(self.testdir, "e"), True, AnimeMovie)
        )
        return base, tv_series, anime_series, movie, anime_movie


class TestVerificatorAbstractClass(TestVerificator):
    """
    Class that tests stuff that's only relevant to the actual abstract
    Verificator class
    """

    structure = {
        "test": {".meta": {}},
    }
    """
    The test directory structure
    """

    metadatas = {
        "test": Base({
            "type": "base",
            "name": "test",
            "tags": []
        })
    }
    """
    The metadata for the media directories
    """

    def test_if_abstract_methods_are_abstract(self):
        """
        Tests if the abstract methods of the Verificator class throw an
        error when called directly
        :return: None
        """

        directory = self.verificators["test"].directory  # type: Directory
        verificator = Verificator(directory, {})

        try:
            verificator.verify()
            self.fail()
        except NotImplementedError:
            pass

        try:
            verificator.fix()
            self.fail()
        except NotImplementedError:
            pass

    def test_for_supported_metadatas(self):
        """
        Tests if supported metadata is identified correctly
        :return: None
        """

        base, tv_series, anime_series, movie, anime_movie = \
            self.generate_sample_metadata()

        # noinspection PyAbstractClass
        class TestClass(Verificator):
            pass

        all_metadata = [base, tv_series, anime_series, movie, anime_movie]
        for config in [
            {
                "types": [Base],
                "valid": all_metadata
            },
            {
                "types": [TvSeries],
                "valid": [tv_series, anime_series]
            },
            {
                "types": [AnimeSeries],
                "valid": [anime_series]
            },
            {
                "types": [TvSeries, AnimeMovie],
                "valid": [tv_series, anime_series, anime_movie]
            },
            {
                "types": [Movie],
                "valid": [movie, anime_movie]
            },
            {
                "types": [AnimeMovie, AnimeSeries],
                "valid": [anime_movie, anime_series]
            }
        ]:
            TestClass.applicable_metadata_types = config["types"]
            for valid in config["valid"]:
                TestClass(valid, {})
            for metadata_type in all_metadata:
                if metadata_type not in config["valid"]:
                    try:
                        TestClass(metadata_type, {})
                        self.fail()
                    except ValueError:
                        pass
