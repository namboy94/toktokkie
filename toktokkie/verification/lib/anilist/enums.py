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

from enum import Enum, auto


class WatchingState(Enum):
    """
    Enum that specifies the watching state of a user's list entry
    """
    CURRENT = auto
    PLANNING = auto
    COMPLETED = auto
    DROPPED = auto
    PAUSED = auto
    REPEATING = auto


class AiringState(Enum):
    """
    Enum that specifies the airing state of a show
    """
    FINISHED = auto
    RELEASING = auto
    NOT_YET_RELEASED = auto
    CANCELLED = auto


class RelationType(Enum):
    """
    Enum that specifies the kind of relation
    two list entries have to each other
    """
    ADAPTATION = auto
    PREQUEL = auto
    SEQUEL = auto
    PARENT = auto
    SIDE_STORY = auto
    CHARACTER = auto
    SUMMARY = auto
    ALTERNATIVE = auto
    SPIN_OFF = auto
    OTHER = auto
