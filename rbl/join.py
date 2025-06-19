import dataclasses
import typing
import sqlalchemy

from sqlalchemy.orm import contains_eager


@dataclasses.dataclass
class Join:
    target: typing.Any | tuple[typing.Any, ...]
    query: typing.Any = None
    onclause: typing.Any = None

    @property
    def query_or_target(self) -> typing.Any:
        return self.query if None is not self.query else self.target_path[-1]
    
    @property
    def target_path(self) -> tuple[typing.Any, ...]:
        if isinstance(self.target, tuple):
            return self.target  # type: ignore
        return (self.target,)


def _to_join(join: typing.Any) -> Join:
    if isinstance(join, Join):
        return join
    return Join(join)


def join_all[*Selectable](queryset: sqlalchemy.Select[tuple[*Selectable]], outerjoins: tuple[typing.Any, ...], innerjoins: tuple[typing.Any, ...]) -> sqlalchemy.Select[tuple[*Selectable]]:
    qs = queryset
    for outerjoin in outerjoins:
        join = _to_join(outerjoin)
        qs = qs.outerjoin(join.query_or_target, join.onclause)
    for innerjoin in innerjoins:
        join = _to_join(innerjoin)
        qs = qs.join(join.query_or_target, join.onclause)
    
    for anyjoin in map(_to_join, [*innerjoins, *outerjoins]):
        kw = {}
        if None is not anyjoin.query:
            kw["alias"] = anyjoin.query
        qs = qs.options(contains_eager(*anyjoin.target_path, **kw))

    return qs


__all__ = ("Join", "join_all")
