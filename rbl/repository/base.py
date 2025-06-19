import typing
import abc

import sqlalchemy

from .proto import Selectable, Bindable, AnySelectable


T = typing.TypeVar("T")
P = typing.ParamSpec("P")
Ts = typing.TypeVarTuple("Ts")

Repository = typing.TypeVar("Repository", bound=AnySelectable)


def queryset_builder(
    func: typing.Callable[typing.Concatenate[Repository, P], sqlalchemy.Select[tuple[*Ts]]],
) -> typing.Callable[typing.Concatenate[Repository, P], Repository]:
    def wrapper(self: Repository, *args: P.args, **kwargs: P.kwargs) -> Repository:
        self.queryset = func(self, *args, **kwargs)
        return self

    return wrapper


class BaseRepository[DataModel, *Columns](abc.ABC, Selectable[*Columns], Bindable[DataModel, *Columns]):
    @abc.abstractmethod
    def select(self) -> sqlalchemy.Select[tuple[*Columns]]:
        ...
    
    @abc.abstractmethod
    def bind(self, *columns: *tuple[*Columns]) -> DataModel:
        ...

    @property
    def queryset(self) -> sqlalchemy.Select[tuple[*Columns]]:
        return self._queryset

    @queryset.setter
    def queryset(self, value: sqlalchemy.Select[tuple[*Columns]], /) -> None:
        self._queryset = value

    def __init__(self) -> None:
        self._queryset = self.select()

    def exists(self) -> sqlalchemy.Select[tuple[bool]]:
        return sqlalchemy.select(sqlalchemy.exists(self.queryset))
    
    def count(self) -> sqlalchemy.Select[tuple[int]]:
        return sqlalchemy.select(sqlalchemy.func.count()).select_from(self.queryset.subquery())
    
    def all(self) -> typing.Self:
        return self


__all__ = ("BaseRepository", "queryset_builder")
