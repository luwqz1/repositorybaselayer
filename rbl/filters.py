from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from sqlalchemy.orm.attributes import QueryableAttribute
    from sqlalchemy.sql.selectable import Select
    from rbl.repository.proto import AnySelectable

from rbl.types import Comparable


def range_filter[Self: AnySelectable, Field: QueryableAttribute[typing.Any]](
    func: typing.Callable[[Self], Field],
):
    def wrapper(
        self: Self,
        min: Comparable | None = None,
        max: Comparable | None = None,
    ) -> Select[typing.Any]:
        field = func(self)
        qs = self.queryset

        if min is not None:
            qs = qs.filter(field >= min)
        if max is not None:
            qs = qs.filter(field <= max)

        return qs

    return wrapper


__all__ = ("range_filter",)
