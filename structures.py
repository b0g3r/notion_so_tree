from dataclasses import dataclass
from numbers import Number
from typing import Iterable, Union


@dataclass
class Field:
    name: str


@dataclass
class RelatedField(Field):
    type = 'related'
    collection_id: str
    related_to: Iterable[str]


@dataclass
class NumberField(Field):
    type = 'number'
    number: Union[float, int]


@dataclass
class TextField(Field):
    type = 'text'
    text: str


@dataclass
class Page:
    id: str
    collection_id: str
    title: str
    fields: Iterable[Field]


@dataclass
class CollectionData:
    id: str
    description: str
    name: str
    pages: Iterable[Page]
