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
from typing import List
from toktokkie.enums import IdType
from toktokkie.metadata.base.components.RenameOperation import RenameOperation
from toktokkie.metadata.base.Renamer import Renamer
from toktokkie.metadata.music.MusicExtras import MusicExtras
from toktokkie.metadata.music.components.MusicThemeSong import \
    MusicThemeSong


class MusicRenamer(Renamer, MusicExtras, ABC):
    """
    Implements the Renamer functionality for music metadata
    """

    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Creates renaming operations for movie metadata
        :return: The renaming operations
        """
        operations = []  # type: List[RenameOperation]

        theme_songs = {x.name: x for x in self.theme_songs}

        for album in self.albums:

            if album.name in theme_songs:
                theme_song = theme_songs[album.name]  # type: MusicThemeSong
                series_name = self.load_title_and_year(
                    [IdType.ANILIST], theme_song.series_ids
                )[0]

                for song in album.songs:
                    if song.title.startswith(theme_song.name):
                        continue  # Skip renaming full version
                    else:
                        new_name = "{} {} - {}.{}".format(
                            series_name,
                            theme_song.theme_type,
                            theme_song.name,
                            song.format
                        )
                        operations.append(RenameOperation(song.path, new_name))

                for vid in album.videos:
                    new_name = "{} {} - {}-video.{}".format(
                        series_name,
                        theme_song.theme_type,
                        theme_song.name,
                        vid.format
                    )
                    operations.append(RenameOperation(vid.path, new_name))
                    break

            else:
                tracks = []
                for song in album.songs:
                    track_number = str(song.tracknumber[0]).zfill(2)
                    videos = [x for x in album.videos if x.title == song.title]
                    video = None if len(videos) == 0 else videos[0]
                    tracks.append((track_number, song, video))

                tracks.sort(key=lambda x: x[0])  # Sort for better UX

                if len(tracks) != 1:
                    for track_number, song, video in tracks:
                        operations.append(RenameOperation(
                            song.path,
                            f"{track_number} - {song.title}.{song.format}"
                        ))
                        if video is not None:
                            operations.append(RenameOperation(
                                video.path,
                                f"{track_number} - {song.title}"
                                f"-video.{video.format}"
                            ))
                else:
                    _, song, video = tracks[0]
                    operations.append(RenameOperation(
                        song.path, f"{album.name}.{song.format}"
                    ))
                    if video is not None:
                        operations.append(RenameOperation(
                            video.path, f"{album.name}-video.{video.format}"
                        ))

        return operations
