from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select


class Selectable[*Columns](typing.Protocol):
    @property
    def queryset(self) -> Select[tuple[*Columns]]: ...

    @queryset.setter
    def queryset(self, value: Select[tuple[*Columns]], /) -> None: ...


class Bindable[DataModel, *Columns](typing.Protocol):
    @classmethod
    def bind(cls, columns: tuple[*Columns]) -> DataModel:
        ...


AnySelectable = Selectable[*tuple[typing.Any, ...]]


__all__ = ("Selectable", "AnySelectable")
