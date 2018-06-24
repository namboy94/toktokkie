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

from toktokkie.verification.lib.anilist.enums import RelationType


class AnilistRelation:
    """
    Class that models an Anilist relation edge
    """

    def __init__(
            self,
            source_mal_id,
            dest_mal_id: int,
            relation_type: RelationType
    ):
        """
        The
        :param source_mal_id: The source myanimelist ID of the edge
        :param dest_mal_id: The destination myanimelist id of the edge
        :param relation_type: The type of relation this edge represents
        """
        self.source_mal_id = source_mal_id
        self.dest_mal_id = dest_mal_id
        self.mal_id = dest_mal_id  # Shortcut for easier access
        self.relation_type = relation_type

    def is_important(self) -> bool:
        """
        Checks if the relation is an important relation or not.
        Adaptation, Character and Alternative relations are deemed unimportant
        :return: True if the relation is an adaptation
        """
        return self.relation_type not in [
            RelationType.ADAPTATION,
            RelationType.CHARACTER,
            RelationType.ALTERNATIVE
        ]
