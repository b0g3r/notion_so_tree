from numbers import Number
from typing import Iterable, Union

import attr


def ensure_pages(values):
    result = []
    for value in values:
        if isinstance(value, Page):
            result.append(value)
        else:
            result.append(Page(**value))
    return result


def ensure_fields(values):
    result = []
    _mapping = {
        'related': RelatedField,
        'number': NumberField,
        'text': TextField,
    }
    for value in values:
        if isinstance(value, Field):
            result.append(value)
        else:
            field_type = value.pop('field_type')
            field_cls = _mapping[field_type]
            result.append(field_cls(**value))
    return result


@attr.s(frozen=True)
class Field:
    name: str = attr.ib()


@attr.s(frozen=True)
class RelatedField(Field):
    collection_id: str = attr.ib()
    related_to: Iterable[str] = attr.ib(factory=list)
    field_type = attr.ib(default='related')


@attr.s(frozen=True)
class NumberField(Field):
    number: Union[float, int] = attr.ib()
    field_type = attr.ib(default='number')


@attr.s(frozen=True)
class TextField(Field):
    text: str = attr.ib()
    field_type = attr.ib(default='text')


@attr.s
class Page:
    id: str = attr.ib()
    collection_id: str = attr.ib()
    title: str = attr.ib()
    fields: Iterable[Field] = attr.ib(factory=list, convert=ensure_fields)


@attr.s
class CollectionData:
    id: str = attr.ib()
    description: str = attr.ib()
    name: str = attr.ib()
    pages: Iterable[Page] = attr.ib(factory=list, convert=ensure_pages)
