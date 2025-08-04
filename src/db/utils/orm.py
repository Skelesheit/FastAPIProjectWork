from typing import Any

from sqlalchemy.orm import Load


def build_filters(cls, kwargs: dict[str, Any]) -> list:
    filters = list()
    for key, value in kwargs.items():
        if value is None or not hasattr(cls, key):
            continue

        column = getattr(cls, key)

        if isinstance(value, str):
            filters.append(column.ilike(f"%{value}%"))

        elif isinstance(value, (list, tuple, set)):
            if all(hasattr(v, 'id') for v in value):
                filters.append(column.in_([v.id for v in value]))
            else:
                filters.append(column.in_(value))

        elif hasattr(value, 'id'):
            filters.append(column == value.id)

        else:
            filters.append(column == value)

    return filters


def apply_load_options(stmt, load_options: list[Load]):
    """
    Прикручивает зависимости при помощи load_options
    :param stmt: изначальный query запросов
    :param load_options: опции load_options()
    :return: None
    """
    if load_options:
        for opt in load_options:
            stmt = stmt.options(opt)
    return stmt
