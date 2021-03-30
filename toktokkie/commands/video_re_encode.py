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
import argparse
from typing import Union, List
from subprocess import check_output, Popen, DEVNULL
from toktokkie.Directory import Directory
from toktokkie.commands.Command import Command
from toktokkie.enums import MediaType
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.metadata.movie.Movie import Movie
from puffotter.os import get_ext


class VideoReEncodeCommand(Command):
    """
    Class that encapsulates behaviour of the video-re-encode command
    """

    ENCODERS = {
        "hevc": [
            "ffmpeg",
            # "-v", "error",-pix_fmt yuv420p10le
            "-i", "INPUT",
            "-c:v", "libx265",
            "-crf", "20",  # lower = better quality, ffmpeg default is 28
            "-c:a", "copy",  # Copy Audio
            "-c:s", "copy",  # Copy Subtitles
            "-map", "0",  # Keep subtitle fonts
            "OUTPUT"
        ],
        "hevc_10": [
            "ffmpeg",
            "-i", "INPUT",
            "-c:v", "libx265",
            "-crf", "18",  # lower = better quality, ffmpeg default is 28
            "-pix_fmt", "yuv420p10le",
            "-c:a", "copy",  # Copy Audio
            "-c:s", "copy",  # Copy Subtitles
            "-map", "0",  # Keep subtitle fonts
            "OUTPUT"
        ]
    }
    """
    The commands used to encode videos
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "video-re-encode"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Allows re-encoding videos files using ffmpeg"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        parser.add_argument("target_encoding", help="The target encoding",
                            choices=cls.ENCODERS.keys())
        parser.add_argument("--anilist-reduce")

    def execute(self):
        """
        Executes the command
        :return: None
        """
        directories = Directory.load_directories(
            self.args.directories,
            restrictions=[MediaType.TV_SERIES, MediaType.MOVIE]
        )
        target_encoding = self.args.target_encoding
        for directory in directories:
            metadata = directory.metadata
            video_files = self.gather_videos(metadata)
            for video_file in reversed(video_files):
                # We go in reverse order to ensure that the newest files are
                # converted first.
                # This is done to reduce risk of accidents, since newer
                # files are probably easier to recover.
                # Also, newer files are probably bigger, increasing the
                # value of re-encoding
                self.re_encode(video_file, target_encoding)

    @staticmethod
    def gather_videos(metadata: Union[Tv, Movie]) -> List[str]:
        """
        Collects all video file paths for a metadata object
        :param metadata: The metadata for which to collect the files
        :return: The collected video file paths
        """
        video_files = []
        if isinstance(metadata, Tv):
            for season in metadata.seasons:
                video_files += season.episode_files
        elif isinstance(metadata, Movie):
            video_files.append(metadata.movie_path)
        return video_files

    @staticmethod
    def get_current_encoding(path: str) -> str:
        """
        Retrieves the current encoding of a video file
        :param path: The path to the file
        :return: The current encoidng of the file
        """
        return check_output([
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_name",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path
        ]).decode("utf-8").strip()

    def re_encode(self, video_file: str, encoding: str):

        current_encoding = self.get_current_encoding(video_file)
        if current_encoding == encoding.replace("_10", ""):
            self.logger.info(f"Skipping {video_file}")
            return

        out_file = os.path.join(
            os.path.dirname(video_file),
            os.path.basename(video_file).rsplit(".", 1)[0] +
            "-re_encode." + get_ext(video_file)
        )
        if os.path.isfile(out_file):
            os.remove(out_file)

        encoder = self.ENCODERS[encoding]
        encoder = [video_file if x == "INPUT" else x for x in encoder]
        encoder = [out_file if x == "OUTPUT" else x for x in encoder]
        print(f"Re-Encoding {video_file} "
              f"from {current_encoding} to {encoding}")
        Popen(encoder, stderr=DEVNULL).wait()
        if os.path.isfile(out_file):
            os.remove(video_file)
            os.rename(out_file, video_file)
        else:
            self.logger.warning(f"Failed to re-encode {video_file}")
