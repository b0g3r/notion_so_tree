from typing import Tuple, Iterable, Dict, List

from networkx import Graph, DiGraph
from pygraphviz import AGraph

from structures import Page, RelatedField, CollectionData


def construct_directed_graph(collections_data: List[CollectionData]) -> AGraph:

    graph = AGraph(directed=True, fontzise=10, fontname='Verdana')
    graph.node_attr['fontname'] = 'Verdana'
    graph.node_attr['shape'] = 'record'

    collection_direction_order_ids = [collection.id for collection in collections_data]
    collection_names = [collection.name for collection in collections_data]

    # draw "y axe" with tree ordering
    graph.add_nodes_from(collection_names, shape='plaintext', fontsize=14)
    graph.add_edges_from(zip(collection_names, collection_names[1:]))
    graph.add_subgraph(collection_names)

    # combine all pages in one graph
    for collection_data in collections_data:
        for page in collection_data.pages:
            node = get_node(page)
            graph.add_node(node, label=page.title)
            # don't include reversed relations:
            edges = get_edges(page, collection_direction_order_ids)
            graph.add_edges_from(edges)

        # align all nodes for one level in one line (include element from "y" line for alignment)
        one_level_nodes = [collection_data.name] + [get_node(page) for page in collection_data.pages]
        graph.add_subgraph(one_level_nodes, None, rank='same')

    return graph


def remove_bad_edges(graph: AGraph, collections: Iterable[Iterable[str]]):
    for from_node, to_node in graph.edges():
        from_group = None
        to_group = None
        for i, group in enumerate(collections):
            if from_node in group:
                from_group = i
            if to_node in group:
                to_group = i
        if from_group is None or to_group is None or from_group < to_group:
            graph.delete_edge(from_node, to_node)


def get_node(page: Page) -> str:
    return page.id


def get_edges(page: Page, collection_order: List[str]) -> Iterable[Tuple[str, str]]:
    edges = []
    from_node = get_node(page)

    # prevent reverted relations
    page_collection_id = page.collection_id
    accepted_collections_from = collection_order.index(page_collection_id)
    accepted_collections = collection_order[accepted_collections_from:]

    for field in page.fields:
        if not isinstance(field, RelatedField):
            continue
        if field.collection_id in accepted_collections:
            edges += [(from_node, to_node) for to_node in field.related_to]

    return edges
