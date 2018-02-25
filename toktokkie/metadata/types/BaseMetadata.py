import json


class MetadataType(object):

    def write(self, json_path: str):
        raise NotImplementedError()

class BaseMetadata(MetadataType):

    @classmethod
    def from_json(cls, path: str) -> MetadataType:
        pass

    def write(self, json_path: str):
        pass

    @staticmethod
    def generate_with_prompt() -> MetadataType:
        pass

    def __init__(self, name: str, tags: list):
        self.type = "base"
        self.name = name
        self.tags = tags


class TvSeriesMetadata(BaseMetadata):

    def __init__(self, name: str, tags: list, seasons: list):
        super().__init__(name, tags)
        self.type = "tv_series"
        self.seasons = []

class MetadataLoader:

    def resolve_directories(self, directory: str, recursive: bool = False):
        pass

    def from_json(self, json_path: str) -> MetadataType:
        with open(json_path, "r") as f:
            json_data = json.load(f)

        if json_data["type"] == "base":
            return