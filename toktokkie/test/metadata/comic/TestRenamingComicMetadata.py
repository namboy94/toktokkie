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
from typing import List, Tuple
from puffotter.os import listdir
from toktokkie.metadata.enums import IdType
from toktokkie.metadata.comic.Comic import Comic
from toktokkie.test.TestFramework import _TestFramework


class TestRenamingComicMetadata(_TestFramework):
    """
    Class that tests the ComicRenamer class
    """

    @staticmethod
    def scramble_comic_chapters(comic: Comic) -> List[Tuple[str, str]]:
        """
        Scrambles comic chapter names
        :param comic: The comic metadata to scramble
        :return: A list of tuples, cojnsisting of the old and new path
        """
        renamed = []
        for content_dir in [comic.main_path, comic.special_path]:
            if not os.path.isdir(content_dir):
                continue
            for item, item_path in listdir(content_dir, no_dirs=True):
                new = os.path.join(content_dir, "Z" + item)
                os.rename(item_path, new)
                renamed.append((item_path, new))
        return renamed

    def test_renaming_comic_metadata(self):
        """
        Tests renaming a comic directory
        :return: None
        """
        path = self.get("Taishou Otome Otogibanashi")
        meta = Comic(path)

        renamed = self.scramble_comic_chapters(meta)

        for old, new in renamed:
            self.assertFalse(os.path.isfile(old))
            self.assertTrue(os.path.isfile(new))

        meta.rename(noconfirm=True)

        for old, new in renamed:
            self.assertTrue(os.path.isfile(old))
            self.assertFalse(os.path.isfile(new))

    def test_renaming_without_special_chapters(self):
        """
        Tests renaming without special chapters
        :return: None
        """
        path = self.get("Taishou Otome Otogibanashi")
        meta = Comic(path)
        meta.special_chapters = []
        shutil.rmtree(meta.special_path)

        renamed = self.scramble_comic_chapters(meta)

        operations = meta.create_rename_operations()
        self.assertEqual(len(operations), len(listdir(meta.main_path)))
        self.assertEqual(len(operations), len(renamed))

    def test_renaming_with_invalid_amount_of_special_chapters(self):
        """
        Tests renaming without special chapters
        :return: None
        """
        path = self.get("Taishou Otome Otogibanashi")
        meta = Comic(path)
        special_chapters = meta.special_chapters
        special_chapters.pop(0)
        meta.special_chapters = special_chapters

        renamed = self.scramble_comic_chapters(meta)

        operations = meta.create_rename_operations()
        self.assertEqual(len(operations), len(listdir(meta.main_path)))
        self.assertNotEqual(len(operations), len(renamed))

    def test_renaming_special_chapter_without_inference(self):
        """
        Tests renaming a comic director's special chapters where one chapter's
        chapter number cannot be inferred
        :return: None
        """
        path = self.get("Taishou Otome Otogibanashi")
        meta = Comic(path)

        renamed = self.scramble_comic_chapters(meta)
        old_non_inferred, current_non_inferred = renamed.pop(-1)
        new_non_inferred = os.path.join(
            meta.special_path, "ZZ - Chapter 1000.cbz"
        )
        os.rename(current_non_inferred, new_non_inferred)
        renamed.append((old_non_inferred, new_non_inferred))

        for old, new in renamed:
            self.assertFalse(os.path.isfile(old))
            self.assertTrue(os.path.isfile(new))

        meta.rename(noconfirm=True)

        for old, new in renamed:
            print(old)
            self.assertTrue(os.path.isfile(old))
            self.assertFalse(os.path.isfile(new))

    def test_renaming(self):
        """
        Tests renaming files associated with the metadata type
        :return: None
        """
        taisho = self.get("Taishou Otome Otogibanashi")
        meta = Comic(taisho)

        def check_files(correct: bool):
            """
            Checks that the files are named correctly
            :param correct: Whether or not the files should be named
                            correctly right now
            :return: None
            """
            for i, _ in enumerate(listdir(meta.main_path)):
                should = "{} - Chapter {}.cbz".format(
                    meta.name,
                    str(i + 1).zfill(2)
                )

                dest = os.path.join(meta.main_path, should)
                self.assertEqual(correct, os.path.isfile(dest))
            for chap in meta.special_chapters:
                should = "{} - Chapter {}.cbz".format(
                    meta.name,
                    chap.zfill(4)
                )
                dest = os.path.join(meta.special_path, should)
                self.assertEqual(correct, os.path.isfile(dest))

        for chapter, path in listdir(meta.main_path):
            os.rename(
                path,
                os.path.join(meta.main_path, "A" + chapter)
            )
        for chapter, path in listdir(meta.special_path):
            os.rename(
                path,
                os.path.join(meta.special_path, "B" + chapter)
            )

        check_files(False)
        meta.rename(noconfirm=True)
        check_files(True)

        meta.set_ids(IdType.ANILIST, ["106988"])
        meta.rename(noconfirm=True)

        self.assertEqual(meta.name, "Shouwa Otome Otogibanashi")
        check_files(True)
