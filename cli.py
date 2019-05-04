from typing import List, Optional

import click

import api
import export


@click.group()
def cli():
    """
    notion_so_tree is a special util which converts related tables and cards from Notion.so
    to tree graph and can visualize it.
    """


@cli.command(
    short_help='Retrieves your collections from notion.so by API and exports theirs to .json file.',
    # TODO: activate it when 7.1 click will released:
    # no_args_is_help=True,
)
@click.argument('api_key')
@click.argument('view_urls', nargs=-1, required=True)
@click.option('--export-file-name', default=None)
def retrieve(api_key: str, view_urls: List[str], export_file_name: Optional[str]):
    """
    Retrieves your collections from notion.so by API and exports theirs to .json file.
    Easiest way to get API_KEY is extract from cookies "token_v2" on notion.so.
    Pass your own API_KEY and few "Collection View" URLs in the order which corresponds
    with tree levels (for example: cities, houses, rooms).
    You can get it in UI wherever there is a "notion database" — tables, cards, etc.
    Just use line "Copy link to View" in database context menu.

    NB: full retrieving is a long process and may take to a few minutes.
    """
    collections = api.get_collections_data(api_key, view_urls)
    real_file_name = export.export_to_json(collections, export_file_name)
    click.echo(real_file_name)


if __name__ == '__main__':
    cli()
