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
from typing import List, Dict, Union
from youtube_dl.YoutubeDL import YoutubeDL
from colorama import Fore, Style
from puffotter.prompt import prompt
from puffotter.os import makedirs, listdir, get_ext
from toktokkie.commands.Command import Command
from toktokkie.exceptions import MissingMetadata, InvalidMetadata
from toktokkie.enums import IdType
from toktokkie.metadata.music.Music import Music
from toktokkie.metadata.music.components.MusicAlbum import MusicAlbum


class YoutubeMusicDlCommand(Command):
    """
    Class that encapsulates behaviour of the youtube-music-dl command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "youtube-music-dl"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Downloads music from youtube"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        parser.add_argument("artist_directory",
                            help="The directory of the artist")
        parser.add_argument("year", type=int, help="The year of the music")
        parser.add_argument("genre", help="The genre of the music")
        parser.add_argument("youtube_urls", nargs="+",
                            help="The youtube video/playlist URLs")
        parser.add_argument("--album-name", help="Specifies an album name for"
                                                 "the downloaded playlist")
        parser.add_argument("--only-audio", action="store_true",
                            help="If specified, discards video files")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        directory = self.args.artist_directory

        # Create directory if it does not exist
        try:
            metadata = Music(directory)
        except MissingMetadata:
            makedirs(directory)
            self.logger.warning("Missing metadata")
            metadata = Music.from_prompt(directory)
            metadata.write()
        except InvalidMetadata:
            self.logger.warning(f"Invalid music metadata for {directory}")
            return

        tmp_dir = "/tmp/toktokkie-ytmusicdl"
        makedirs(tmp_dir, delete_before=True)

        downloaded = self.download_from_youtube(tmp_dir)
        self.create_albums(metadata, downloaded)
        metadata.rename(noconfirm=True)

    def download_from_youtube(self, target_dir: str) \
            -> List[Dict[str, Union[str, Dict[str, str]]]]:
        """
        Downloads all youtube URLs from the command line arguments into a
        directory. Both mp4 and mp3 files will be downloaded if not specified
        otherwise by command line arguments.
        Playlists will be resolved to their own video IDs and downloaded
        seperately
        :param target_dir: The directory in which to store the downloaded files
        :return: The downloaded songs in the following form:
                 [{"files": {extension: path}}, "id": "ID"}, ...]
        """
        mp3_args = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": f"{target_dir}/%(title)s.%(ext)s",
            "ignoreerrors": True
        }
        mp4_args = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": f"{target_dir}/%(title)s-video.%(ext)s",
            "ignoreerrors": True
        }

        youtube_dl_args = [mp3_args]
        if not self.args.only_audio:
            youtube_dl_args.append(mp4_args)

        video_ids = []
        with YoutubeDL() as yt_info:
            for youtube_url in self.args.youtube_urls:
                url_info = yt_info.extract_info(youtube_url, download=False)
                if url_info.get("_type") == "playlist":
                    for entry in url_info["entries"]:
                        video_ids.append(entry["id"])
                else:
                    video_ids.append(url_info["id"])

        directory_content = []
        downloaded = []
        for video_id in video_ids:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            for args in youtube_dl_args:
                with YoutubeDL(args) as youtube_dl:
                    youtube_dl.download([video_url])

            new_content = sorted([
                x[1] for x in listdir(target_dir)
                if x[1] not in directory_content
            ])
            directory_content += new_content

            files = {get_ext(x): x for x in new_content}
            mp3_file = os.path.basename(files["mp3"])
            mp3_name = mp3_file.rsplit(".mp3", 1)[0]

            entry = {
                "id": video_id,
                "files": files,
                "name": mp3_name
            }
            downloaded.append(entry)

        for entry in downloaded:
            entry["name"] = prompt(
                f"Enter song name for "
                f"{Fore.LIGHTYELLOW_EX}{entry['name']}{Style.RESET_ALL}",
                required=True
            )

        return downloaded

    def create_albums(
            self,
            music: Music,
            info: List[Dict[str, Union[str, Dict[str, str]]]]
    ):
        """
        Creates album objects based on downloaded info
        :param music: The music metadata
        :param info: The info from youtube download
        :return: None
        """
        existing = [x.name for x in music.albums]
        if self.args.album_name is not None:

            if self.args.album_name in existing:
                self.logger.warning(
                    f"Album {self.args.album_name} already exists"
                )
                return

            album = MusicAlbum(
                music.directory_path,
                music.ids,
                {IdType.YOUTUBE_VIDEO: [x["id"] for x in info]},
                self.args.album_name,
                self.args.genre,
                self.args.year
            )
            makedirs(album.path)
            music.add_album(album)

            order = self.prompt_song_order([x["name"] for x in info])
            for entry in info:
                index = str(order.index(entry["name"])).zfill(len(order))
                for ext, path in entry["files"].items():
                    shutil.move(path, os.path.join(
                        album.path,
                        f"{index} - {entry['name']}.{ext}"
                    ))
        else:
            for entry in info:
                album = MusicAlbum(
                    music.directory_path,
                    music.ids,
                    {IdType.YOUTUBE_VIDEO: [entry["id"]]},
                    entry["name"],
                    self.args.genre,
                    self.args.year
                )
                if album.name in existing:
                    self.logger.warning(f"Album {album.name} already exists")
                    continue
                else:
                    makedirs(album.path)
                    music.add_album(album)
                    for ext, path in entry["files"].items():
                        print(path)
                        shutil.move(
                            path,
                            os.path.join(album.path, f"{entry['name']}.{ext}")
                        )

        music.write()

    @staticmethod
    def prompt_song_order(names: List[str]) -> List[str]:
        """
        Prompts the user for the song order in an album
        :param names: The names of the songs
        :return: List of ordered song names
        """
        ordered = []
        while len(names) > 1:
            for i, song in enumerate(names):
                print(f"{i + 1} - {song}")
            index = prompt(
                "Next song in order: ",
                _type=int,
                choices={str(x) for x in range(1, len(names) + 1)}
            ) - 1
            selected = names.pop(index)
            ordered.append(selected)

        assert len(names) == 1
        ordered.append(names.pop(0))

        return ordered
