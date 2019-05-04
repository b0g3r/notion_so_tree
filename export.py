import json
from datetime import datetime
from typing import List

import attr

from structures import CollectionData


def export_to_json(collections_data: List[CollectionData], file_name: str = None) -> str:
    """
    Small helper for exporting list of collection data to json format.
    """
    native_python = [attr.asdict(collection_data) for collection_data in collections_data]

    if file_name is None:
        file_name = 'exported_collections_{0:%Y-%m-%d-%H:%M:%S}.json'.format(datetime.now())

    json.dump(native_python, open(file_name, 'w'))
    return file_name
