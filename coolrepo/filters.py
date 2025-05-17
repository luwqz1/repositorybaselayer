from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from sqlalchemy.orm.attributes import QueryableAttribute
    from sqlalchemy.sql.selectable import Select
    from coolrepo.repository.abc import ABCRepository

type Numeric = int | float
type RangeFilter[Repository: ABCRepository] = typing.Callable[
    [Repository, Numeric | None, Numeric | None],
    typing.Any,
]


def range_filter[Repository: ABCRepository, Field: QueryableAttribute](
    func: typing.Callable[[], Field],
) -> RangeFilter[Repository]:
    def wrapper(
        self: Repository,
        gte: Numeric | None = None,
        lte: Numeric | None = None,
    ) -> Select[typing.Any]:
        field = func()
        qs = self.queryset

        if gte is not None:
            qs = qs.filter(field >= gte)
        if lte is not None:
            qs = qs.filter(field <= lte)

        return qs

    return wrapper


__all__ = ("range_filter",)
