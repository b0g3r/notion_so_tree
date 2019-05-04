from typing import IO, Iterable, Tuple

from structures import Field, RelatedField, TextField, Page


def parse_page_file(page_raw: str, type: str, file_name: str) -> Page:
    """
    FIXME: add documentation
    """
    page_id = extract_page_id(file_name)
    title, fields = parse_md(page_raw)
    return Page(
        id=page_id,
        type=type,
        title=title,
        fields=fields,
    )


def extract_page_id(full_file_name: str) -> str:
    """
    Extract page id from file_name

    Example:
        Data-loss-94d44921-0a4c-4319-8f78-60ef45267d97.md -> 94d449210a4c43198f7860ef45267d97

    """
    file_name, _ = full_file_name.rsplit('.', maxsplit=1)
    parts = file_name.rsplit('-', maxsplit=5)
    id_parts = parts[-5:]
    return ''.join(id_parts)


def parse_md(page: str) -> Tuple[str, Iterable[Field]]:
    """
    Extract fields and title from file content.
    """
    lines = [line for line in page.split('\n') if line]
    title = lines[0].strip('# ')
    title = title.replace('>', 'greater than')
    title = title.replace('<', 'less than')

    content_raw = ""
    fields = []

    for line in lines[1:]:
        # FIXME: move block about field parsing into new function
        if ':' in line:
            field_name, field_raw = line.split(':', maxsplit=1)
            field_parts = field_raw.split(',')
            if all([part.strip().startswith('https://www.notion.so/') for part in field_parts]):
                linked_ids = [part.strip()[22:] for part in field_parts]
                field = RelatedField(
                    name=field_name,
                    linked_pages=linked_ids,
                )
            else:
                field = TextField(
                    name=field_name,
                    text=field_raw,
                )
            fields.append(field)
        else:
            content_raw += line + '\n'

    if content_raw:
        content_field = TextField(
            name='_content',
            text=content_raw,
        )
        fields.append(content_field)

    return title, fields
