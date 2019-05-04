import json
from typing import List

from structures import CollectionData


def import_from_json(file_name: str) -> List[CollectionData]:
    """
    Simple helper which import list of collections data from json file by filename.
    """
    raw = json.load(open(file_name))
    return [
        CollectionData(**raw_collection_data) for raw_collection_data in raw
    ]
