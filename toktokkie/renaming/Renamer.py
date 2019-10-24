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
import logging
from typing import List, Optional, Dict
from puffotter.os import listdir, replace_illegal_ntfs_chars, get_ext
from puffotter.prompt import yn_prompt
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.types.TvSeries import TvSeries
from toktokkie.metadata.types.Manga import Manga
from toktokkie.metadata.types.MusicArtist import MusicArtist
from toktokkie.metadata.types.components.MusicThemeSong import MusicThemeSong
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.MediaType import MediaType
from toktokkie.renaming.RenameOperation import RenameOperation
from toktokkie.renaming.functions import generate_tv_episode_filename, \
    load_tvdb_episode_name
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.Title import TitleType
from anime_list_apis.models.attributes.MediaType import MediaType as \
    AnilistMediaType


class Renamer:
    """
    Class that handles the renaming of a media directory's content
    """

    def __init__(self, metadata: Metadata):
        """
        Initializes the Renamer. ValueErrors will be thrown if an error
        is encountered at any point during the initialization process
        :param metadata: The metadata to use for information
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.metadata = metadata
        self.operations = self._generate_operations()

    @property
    def path(self) -> str:
        """
        :return: The path to the media directory
        """
        return self.metadata.directory_path

    def _generate_operations(self) -> List[RenameOperation]:
        """
        Generates renaming operations for the various possible media types
        :return: The renaming operations
        """
        operations = []  # type: List[RenameOperation]
        if self.metadata.media_type() == MediaType.BOOK:
            operations = self._generate_book_operations()
        elif self.metadata.media_type() == MediaType.BOOK_SERIES:
            operations = self._generate_book_series_operations()
        elif self.metadata.media_type() == MediaType.MOVIE:
            operations = self._generate_movie_operations()
        elif self.metadata.media_type() == MediaType.TV_SERIES:
            operations = self._generate_tv_series_operations()
        elif self.metadata.media_type() == MediaType.MANGA:
            operations = self._generate_manga_operations()
        elif self.metadata.media_type() == MediaType.MUSIC_ARTIST:
            operations = self._generate_music_operations()
        elif self.metadata.media_type() == MediaType.VISUAL_NOVEL:
            pass
        else:
            self.logger.error("Renaming methods for {} not implemented"
                              .format(self.metadata.media_type().name))
        return operations

    def get_active_operations(self) -> List[RenameOperation]:
        """
        :return: Any rename operations whose source and destination
                 paths differ.
        """
        return list(filter(lambda x: x.source != x.dest, self.operations))

    def rename(self, noconfirm: bool):
        """
        Renames the contained files according to the naming schema.
        :param noconfirm: Skips the confirmation phase if True
        :return: None
        """
        should_title = self.load_title_name()
        if should_title != self.metadata.name:
            ok = noconfirm
            if not ok:
                ok = yn_prompt("Rename title of series to {}?"
                               .format(should_title))
            if ok:
                self.metadata.name = should_title
                self.operations = self._generate_operations()

        if len(self.get_active_operations()) == 0:
            self.logger.info("Files already named correctly, skipping.")
            return

        if not noconfirm:
            for operation in self.operations:
                print(operation)

            prompt = yn_prompt("Proceed with renaming?")

            if not prompt:
                self.logger.warning("Renaming aborted.")
                return

        for operation in self.operations:
            operation.rename()

    def load_title_name(
            self,
            id_override: Optional[Dict[IdType, List[str]]] = None
    ) -> str:
        """
        Loads the title name for the metadata object
        :param id_override: Uses other IDs than in the metadata
        :return: The title the metadata should have
        """
        should_name = self.metadata.name

        ids = id_override if id_override is not None else self.metadata.ids

        anilist = ids.get(IdType.ANILIST, [])
        if len(anilist) > 0:
            anilist_id = int(anilist[0])
            media_type = AnilistMediaType.ANIME
            if self.metadata.media_type() in [
                MediaType.BOOK, MediaType.BOOK_SERIES, MediaType.MANGA
            ]:
                media_type = AnilistMediaType.MANGA
            entry = AnilistApi().get_data(media_type, anilist_id)
            should_name = entry.title.get(TitleType.ENGLISH)

            if self.metadata.media_type() == MediaType.MOVIE:
                should_name += " ({})".format(entry.releasing_start.year)

        return replace_illegal_ntfs_chars(should_name)

    def _get_children(self, no_dirs: bool = False, no_files: bool = False) \
            -> List[str]:
        """
        Retrieves a list of files and/or directories inside the media directory
        that may be valid for renaming
        :param no_dirs: If True, will ignore all directories
        :param no_files: If True, will ignore all files
        :return: A list of child directories/files, excluding hidden or
                 metadata files.
        """
        children = []
        for child in os.listdir(self.path):
            if child.startswith("."):
                continue
            elif os.path.isdir(os.path.join(self.path, child)) and no_dirs:
                continue
            elif os.path.isfile(os.path.join(self.path, child)) and no_files:
                continue
            else:
                children.append(child)

        return sorted(children)

    def _generate_book_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for book media types
        :return: The list of rename operations
        """
        book_file = self._get_children(no_dirs=True)[0]
        dest = "{}.{}".format(self.metadata.name, get_ext(book_file))
        return [RenameOperation(
            os.path.join(self.path, book_file), dest
        )]

    def _generate_manga_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for manga media types
        :return: The list of rename operations
        """
        # noinspection PyTypeChecker
        metadata = self.metadata  # type: Manga  # type: ignore

        main_content = listdir(metadata.main_path, no_dirs=True)
        max_chapter_length = len(str(len(main_content)))

        operations = []

        for i, (old_name, old_path) in enumerate(main_content):
            ext = old_name.rsplit(".", 1)[1]
            new_name = "{} - Chapter {}.{}".format(
                metadata.name,
                str(i + 1).zfill(max_chapter_length),
                ext
            )
            operations.append(RenameOperation(old_path, new_name))

        if not os.path.isdir(metadata.special_path):
            return operations

        special_content = listdir(metadata.special_path, no_dirs=True)

        if len(special_content) != len(metadata.special_chapters):
            self.logger.warning(
                "Invalid amount of special chapters!!! {} != {}".format(
                    len(special_content), len(metadata.special_chapters)
                )
            )
            return operations
        else:
            special_max_length = len(max(
                metadata.special_chapters,
                key=lambda x: len(x)
            ))
            for i, (old_name, old_path) in enumerate(special_content):
                chap_guess, ext = old_name.rsplit(".", 1)

                chapter_num = metadata.special_chapters[i]

                # Tries to infer the chapter number from local files.
                # Useful if a newly added chapter does not fit correctly
                # in the lexicological order
                try:
                    chap_guess = chap_guess.rsplit(" - Chapter ", 1)[1]
                    while chap_guess.startswith("0"):
                        chap_guess = chap_guess[1:]
                    if chap_guess in metadata.special_chapters:
                        chapter_num = chap_guess

                except IndexError:
                    pass

                new_name = "{} - Chapter {}.{}".format(
                    metadata.name,
                    chapter_num.zfill(special_max_length),
                    ext
                )
                operations.append(RenameOperation(old_path, new_name))

        return operations

    def _generate_book_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for book series media types
        :return: The list of rename operations
        """
        operations = []
        children = self._get_children(no_dirs=True)
        fill = len(str(len(children)))

        for i, volume in enumerate(children):
            ext = volume.rsplit(".", 1)[1]
            new_name = "{} - Volume {}.{}".format(
                self.metadata.name,
                str(i + 1).zfill(fill),
                ext
            )

            operations.append(RenameOperation(
                os.path.join(self.path, volume), new_name
            ))

        return operations

    def _generate_music_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for music artist media types
        :return: The list of rename operations
        """
        operations = []  # type: List[RenameOperation]

        # noinspection PyTypeChecker
        music_metadata = self.metadata  # type: MusicArtist  # type: ignore
        music_exts = ["mp3", "flac", "wav"]
        video_exts = ["mp4", "webm", "mkv", "avi"]

        theme_songs = {x.name: x for x in music_metadata.theme_songs}

        for album in music_metadata.albums:
            song_files = listdir(album.path)

            if album.name in theme_songs:
                theme_song = theme_songs[album.name]  # type: MusicThemeSong
                series_name = \
                    self.load_title_name(id_override=theme_song.series_ids)

                for song, path in song_files:
                    if song.startswith(theme_song.name):
                        continue  # Skip renaming full version

                    ext = get_ext(song)
                    if ext in video_exts:
                        new_name = "{} {} - {}-video.{}".format(
                            series_name,
                            theme_song.theme_type,
                            theme_song.name,
                            ext
                        )
                        operations.append(RenameOperation(path, new_name))
                    elif ext in music_exts:
                        new_name = "{} {} - {}.{}".format(
                            series_name,
                            theme_song.theme_type,
                            theme_song.name,
                            ext
                        )
                        operations.append(RenameOperation(path, new_name))
            else:
                for i, (song, path) in enumerate(song_files):
                    track_number = str(i + 1).zfill(2)

                    if song.split(" - ")[0].isnumeric():
                        if not song.startswith(track_number + " - "):
                            operations.append(RenameOperation(
                                path,
                                track_number + " - " + song.split(" - ", 1)[1]
                            ))
                    else:
                        operations.append(RenameOperation(
                            path,
                            track_number + " - " + song
                        ))

        return operations

    def _generate_movie_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for movie media types
        :return: The list of rename operations
        """
        movie_file = self._get_children(no_dirs=True)[0]
        dest = "{}.{}".format(self.metadata.name, get_ext(movie_file))
        return [RenameOperation(
            os.path.join(self.path, movie_file), dest
        )]

    def _generate_tv_series_operations(self) -> List[RenameOperation]:
        """
        Generates rename operations for tv series media types
        :return: The list of rename operations
        """
        operations = []

        # noinspection PyTypeChecker
        tv_series_metadata = self.metadata  # type: TvSeries  # type: ignore

        excluded = tv_series_metadata.excludes.get(IdType.TVDB, {})
        multis = tv_series_metadata.multi_episodes.get(IdType.TVDB, {})
        start_overrides = \
            tv_series_metadata.season_start_overrides.get(IdType.TVDB, {})

        content_info = tv_series_metadata.get_episode_files()

        for tvdb_id, season_data in content_info.items():
            tvdb_ids = tv_series_metadata.ids.get(IdType.TVDB, [])
            is_spinoff = tvdb_ids[0] != tvdb_id

            if is_spinoff:
                sample_episode = season_data[list(season_data)[0]][0]
                location = os.path.dirname(sample_episode)
                series_name = os.path.basename(location)
            else:
                series_name = tv_series_metadata.name

            for _season_number, episodes in season_data.items():
                season_number = _season_number if not is_spinoff else 1

                season_excluded = excluded.get(season_number, [])
                season_multis = multis.get(season_number, {})
                episode_number = start_overrides.get(season_number, 1)

                for episode_file in episodes:

                    while episode_number in season_excluded:
                        episode_number += 1

                    if episode_number not in season_multis:
                        end = None  # type: Optional[int]
                    else:
                        end = season_multis[episode_number]

                    episode_name = load_tvdb_episode_name(
                        tvdb_id, season_number, episode_number, end
                    )

                    new_name = generate_tv_episode_filename(
                        episode_file,
                        series_name,
                        season_number,
                        episode_number,
                        episode_name,
                        end
                    )

                    if end is not None:
                        episode_number = end

                    operations.append(RenameOperation(episode_file, new_name))
                    episode_number += 1

        return operations
