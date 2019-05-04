"""
Methods for working with Notion.so API. Uses [notion-py](https://github.com/jamalex/notion-py)
"""
from typing import Iterable, List

from notion.client import NotionClient
from notion.collection import Collection, CollectionRowBlock

from structures import Page, NumberField, TextField, RelatedField, CollectionData


# TODO: rewrite this module to app agnostic (without `structures`)
# move convert_collection_row to another module


def get_collections_data(api_key: str, collection_views_urls: Iterable[str]) -> List[CollectionData]:
    """
    Get collection data (info + pages) from Notion.so API by collection view url list.
    """
    client = NotionClient(api_key)
    collections_data = [
        get_collection_data(client, url) for url in collection_views_urls
    ]
    return collections_data


def get_collection_data(client: NotionClient, collection_view_url) -> CollectionData:
    collection = get_collection(client, collection_view_url)
    collection_rows = get_collection_rows(collection)
    collection_pages = [convert_collection_row(row) for row in collection_rows]
    collection_info = combine_collection_data(collection, collection_pages)
    return collection_info


def combine_collection_data(collection: Collection, pages: Iterable[Page]) -> CollectionData:
    return CollectionData(
        id=collection.id,
        name=collection.name,
        description=collection.description,
        pages=pages,
    )


def get_collection(client: NotionClient, collection_view_url: str) -> Collection:
    collection_view = client.get_collection_view(collection_view_url)
    return collection_view.collection

def get_collection_rows(collection: Collection) -> Iterable[CollectionRowBlock]:
    all_rows = collection.get_rows()
    return all_rows


def convert_collection_row(row: CollectionRowBlock) -> Page:
    page_title = row.title
    page_title = page_title.replace('>', 'greater than')
    page_title = page_title.replace('<', 'less than')

    page_id = row.id
    page_collection_id = row.collection.id
    properties = row.get_all_properties()
    page_fields = []
    for property_name, property_value in properties.items():
        if isinstance(property_value, (int, float)):
            page_fields.append(
                NumberField(
                    name=property_name,
                    number=property_value,
                )
            )
        elif isinstance(property_value, str):
            page_fields.append(
                TextField(
                    name=property_name,
                    text=property_value,
                )
            )
        elif isinstance(property_value, list):
            # Eventually first element of related field is None. I don't know why
            filtered_list = list(filter(lambda el: el is not None, property_value))
            if len(filtered_list) > 0 and all(isinstance(el, CollectionRowBlock) for el in filtered_list):
                collection_id = filtered_list[0].collection.id
                page_fields.append(
                    RelatedField(
                        name=property_name,
                        collection_id=collection_id,
                        related_to=[block.id for block in filtered_list]
                    )
                )
    return Page(
        id=page_id,
        collection_id=page_collection_id,
        title=page_title,
        fields=page_fields
    )