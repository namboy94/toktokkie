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
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.utils.RenameOperation import RenameOperation
from toktokkie.neometadata.base.Renamer import Renamer
from toktokkie.neometadata.comic.ComicExtras import ComicExtras


class ComicRenamer(Renamer, ComicExtras, ABC):
    """
    Implements the Renamer functionality for comic metadata
    """

    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Creates renaming operations for book series metadata
        :return: The renaming operations
        """
        main_content = listdir(self.main_path, no_dirs=True)
        max_chapter_length = len(str(len(main_content)))

        operations = []

        for i, (old_name, old_path) in enumerate(main_content):
            ext = old_name.rsplit(".", 1)[1]
            new_name = "{} - Chapter {}.{}".format(
                self.name,
                str(i + 1).zfill(max_chapter_length),
                ext
            )
            operations.append(RenameOperation(old_path, new_name))

        if not os.path.isdir(self.special_path):
            return operations

        special_content = listdir(self.special_path, no_dirs=True)

        if len(special_content) != len(self.special_chapters):
            self.logger.warning(
                "Invalid amount of special chapters!!! {} != {}".format(
                    len(special_content), len(self.special_chapters)
                )
            )
            return operations
        else:
            special_max_length = len(max(
                self.special_chapters,
                key=lambda x: len(x)
            ))
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

                new_name = "{} - Chapter {}.{}".format(
                    self.name,
                    chapter_num.zfill(special_max_length),
                    ext
                )
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
