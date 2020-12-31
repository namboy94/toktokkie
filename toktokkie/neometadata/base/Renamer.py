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

from abc import ABC
from imdb import IMDb
from typing import List, Tuple, Optional
from puffotter.prompt import yn_prompt
from puffotter.os import replace_illegal_ntfs_chars
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.Title import TitleType
from anime_list_apis.models.attributes.MediaType import MediaType as \
    AnilistMediaType
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.base.MetadataBase import MetadataBase
from toktokkie.neometadata.utils.RenameOperation import RenameOperation
from toktokkie.neometadata.utils.ids import literature_media_types


class Renamer(MetadataBase, ABC):
    """
    Class that's responsible to define renaming functionality
    """

    def rename(self, noconfirm: bool, skip_title: bool = False):
        """
        Renames the contained files according to the naming schema.
        :param noconfirm: Skips the confirmation phase if True
        :param skip_title: If True, will skip title renaming
        :return: None
        """
        if skip_title:
            should_title = self.name
        else:
            should_title = self.resolve_title_name()

        operations = self.create_rename_operations()

        if should_title != self.name:
            if noconfirm or \
                    yn_prompt(f"Rename title of series to {should_title}?"):
                self.name = should_title
                # Reload with new title name
                operations = self.create_rename_operations()

        active_operations = list(filter(
            lambda x: x.source != x.dest,
            operations
        ))
        if len(active_operations) == 0:
            self.logger.info("Files already named correctly, skipping.")
            return

        if not noconfirm:
            for operation in operations:
                print(operation)

            prompt = yn_prompt("Proceed with renaming?")

            if not prompt:
                self.logger.warning("Renaming aborted.")
                return

        for operation in operations:
            operation.rename()

    def resolve_title_name(self) -> str:
        """
        If possible, will fetch the appropriate name for the
        metadata based on IDs, falling back to the
        directory name if this is not possible or supported.
        """
        return self.name  # pragma: no cover

    # noinspection PyMethodMayBeStatic
    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Performs rename operations on the content referenced by
        this metadata object
        :return: The rename operations for this metadata
        """
        return []  # pragma: no cover

    def load_anilist_title_and_year(self) -> Tuple[str, Optional[int]]:
        """
        Loads the title and year of an item using anilist IDs
        :return: The title of the item and the year as a tuple
        """
        anilist_ids = self.ids[IdType.ANILIST]
        if len(anilist_ids) == 0:
            return self.name, None

        anilist_id = int(anilist_ids[0])

        if anilist_id == 0:
            return self.name, None

        if self.media_type() in literature_media_types:
            media_type = AnilistMediaType.MANGA
        else:
            media_type = AnilistMediaType.ANIME

        entry = AnilistApi().get_data(media_type, anilist_id)
        new_name = entry.title.get(TitleType.ENGLISH)
        year = entry.releasing_start.year

        return replace_illegal_ntfs_chars(new_name), year

    def load_imdb_title_and_year(self) -> Tuple[str, Optional[int]]:
        """
        Loads the title and year of an item using IMDB IDs
        :return: The title of the item and the year as a tuple
        """
        imdb_ids = self.ids[IdType.IMDB]
        if len(imdb_ids) == 0:
            return self.name, None

        imdb_id = imdb_ids[0].replace("t", "")

        if imdb_id == "0":
            return self.name, None

        info = IMDb().get_movie(imdb_id).data

        new_name = info["title"]
        year = info["year"]

        return replace_illegal_ntfs_chars(new_name), year

    def load_title_and_year(
            self, id_type_priority: List[IdType]
    ) -> Tuple[str, Optional[int]]:
        """
        Loads the title and year based on a custom order of id types
        """
        func_map = {
            IdType.IMDB: self.load_imdb_title_and_year,
            IdType.ANILIST: self.load_anilist_title_and_year
        }

        for id_type in id_type_priority:
            func = func_map.get(id_type, lambda: (self.name, None))
            name, year = func()
            if year is not None:
                return name, year
        return self.name, None
