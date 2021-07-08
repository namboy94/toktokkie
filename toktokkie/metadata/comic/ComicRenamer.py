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
from abc import ABC
from typing import List
from puffotter.os import listdir
from toktokkie.enums import IdType
from manga_dl.entities.Chapter import Chapter
from manga_dl.scrapers.mangadex import MangaDexScraper
from toktokkie.metadata.base.components.RenameOperation import RenameOperation
from toktokkie.metadata.base.Renamer import Renamer
from toktokkie.metadata.comic.ComicExtras import ComicExtras


class ComicRenamer(Renamer, ComicExtras, ABC):
    """
    Implements the Renamer functionality for comic metadata
    """

    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Creates renaming operations for book series metadata
        :return: The renaming operations
        """
        mangadex_chapters = []
        mangadex_ids = self.ids[IdType.MANGADEX]
        if len(mangadex_ids) >= 1:
            mangadex_id = mangadex_ids[0]
            mangadex_chapters = \
                MangaDexScraper().load_chapters(None, mangadex_id)

        operations: List[RenameOperation] = []
        operations += self.__create_main_chapter_operations(mangadex_chapters)
        operations += self.__create_main_volume_operations()
        operations += self.__create_special_chapter_operations(
            mangadex_chapters
        )
        return operations

    def __create_main_chapter_operations(self, mangadex_chapters: List[Chapter]) -> List[RenameOperation]:
        if not os.path.isdir(self.main_chapters_path):
            return []
        main_content = listdir(self.main_chapters_path, no_dirs=True)
        max_chapter_length = len(str(len(main_content)))

        chapter_titles = {}
        for chapter in mangadex_chapters:
            chapter_nr = chapter.chapter_number.zfill(max_chapter_length)
            chapter_titles[chapter_nr] = chapter.title

        operations = []
        offset = self.chapter_offset

        for i, (old_name, old_path) in enumerate(main_content):
            ext = old_name.rsplit(".", 1)[1]
            chapter_number = str(i + 1 + offset).zfill(max_chapter_length)
            chapter_title = chapter_titles.get(chapter_number)
            new_name = f"{self.name} - Chapter {chapter_number}"
            if chapter_title is not None:
                new_name += f" - {chapter_title}"
            new_name += f".{ext}"
            operations.append(RenameOperation(old_path, new_name))
        return operations

    def __create_main_volume_operations(self) -> List[RenameOperation]:
        if not os.path.isdir(self.main_volumes_path):
            return []
        main_content = listdir(self.main_volumes_path, no_dirs=True)
        max_volume_length = len(str(len(main_content)))

        operations = []

        for i, (old_name, old_path) in enumerate(main_content):
            ext = old_name.rsplit(".", 1)[1]
            new_name = "{} - Volume {}.{}".format(
                self.name,
                str(i + 1).zfill(max_volume_length),
                ext
            )
            operations.append(RenameOperation(old_path, new_name))
        return operations

    def __create_special_chapter_operations(self, mangadex_chapters: List[Chapter]) -> List[RenameOperation]:
        if not os.path.isdir(self.special_path):
            return []

        special_content = listdir(self.special_path, no_dirs=True)
        if len(special_content) == 0:
            return []

        if len(special_content) != len(self.special_chapters):
            self.logger.warning(
                "Invalid amount of special chapters!!! {} != {}".format(
                    len(special_content), len(self.special_chapters)
                )
            )
            return []
        else:
            operations: List[RenameOperation] = []
            special_max_length = len(max(
                self.special_chapters,
                key=lambda x: len(x)
            ))

            chapter_titles = {}
            for chapter in mangadex_chapters:
                chapter_nr = chapter.chapter_number.zfill(special_max_length)
                chapter_titles[chapter_nr] = chapter.title

            for i, (old_name, old_path) in enumerate(special_content):
                chap_guess, ext = old_name.rsplit(".", 1)

                chapter_num = self.special_chapters[i]

                # Tries to infer the chapter number from local files.
                # Useful if a newly added chapter does not fit correctly
                # in the lexicological order
                try:
                    chap_guess = chap_guess.rsplit(" - Chapter ", 1)[1]
                    while chap_guess.startswith("0"):
                        chap_guess = chap_guess[1:]
                    if chap_guess in self.special_chapters:
                        chapter_num = chap_guess

                except IndexError:
                    pass

                chapter_nr_formatted = chapter_num.zfill(special_max_length)
                title = chapter_titles.get(chapter_nr_formatted)
                new_name = f"{self.name} - Chapter {chapter_nr_formatted}"
                if title is not None:
                    new_name += f" - {title}"
                new_name += f".{ext}"
                operations.append(RenameOperation(old_path, new_name))
            return operations

    def resolve_title_name(self) -> str:
        """
        If possible, will fetch the appropriate name for the
        metadata based on IDs, falling back to the
        directory name if this is not possible or supported.
        """
        return self.load_title_and_year([
            IdType.ANILIST
        ])[0]
