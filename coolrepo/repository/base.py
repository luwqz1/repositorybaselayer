import typing

import sqlalchemy


from coolrepo.repository.abc import ABCRepository
from coolrepo.tools.func import classproperty
from coolrepo.tools.magic import get_generic_arguments
from coolrepo.join import Join, join_all


Model = typing.TypeVar("Model")
Repository = typing.TypeVar("Repository", bound=ABCRepository)
P = typing.ParamSpec("P")
Ts = typing.TypeVarTuple("Ts")


def queryset_builder(
    func: typing.Callable[typing.Concatenate[Repository, P], sqlalchemy.Select[tuple[*Ts]]],
) -> typing.Callable[typing.Concatenate[Repository, P], Repository]:
    def wrapper(self: Repository, *args: P.args, **kwargs: P.kwargs) -> Repository:
        self.queryset = func(self, *args, **kwargs)
        return self

    return wrapper


class BaseRepository[Model, DataModel = Model, *Selectable = *tuple[Model]](ABCRepository):
    pk_field_name: str = "uuid"

    outerjoins: tuple[typing.Any | Join, ...] = ()
    innerjoins: tuple[typing.Any | Join, ...] = ()

    if typing.TYPE_CHECKING:
        model: type[Model]
    else:
        @classproperty
        def model(cls):
            return get_generic_arguments(cls, BaseRepository).unwrap()[0]

    @classmethod
    def bind(cls, row: tuple[*Selectable]) -> DataModel:
        return row[0]  # type: ignore

    @classmethod
    def select(cls) -> sqlalchemy.Select[tuple[*Selectable]]:
        return sqlalchemy.select(cls.model).filter()  # type: ignore

    @queryset_builder
    def paginate(self, page: int, per_page: int) -> sqlalchemy.Select[tuple[*Selectable]]:
        return self.queryset.order_by(getattr(self.model, self.pk_field_name).asc()).limit(per_page).offset((page - 1) * per_page)

    @queryset_builder
    def get(self, uuid: str) -> sqlalchemy.Select[tuple[*Selectable]]:
        return self.queryset.filter(getattr(self.model, self.pk_field_name) == uuid)
    
    @classmethod
    def create(cls, instance: Model) -> sqlalchemy.Insert:
        return sqlalchemy.insert(cls.model).values(**instance)

    @property
    def queryset(self) -> sqlalchemy.Select[tuple[*Selectable]]:
        return self._queryset

    @queryset.setter
    def queryset(self, value: sqlalchemy.Select[tuple[*Selectable]], /) -> None:
        self._queryset = value

    def __init__(self) -> None:
        self._queryset = self.select()
        self._queryset = join_all(self._queryset, self.outerjoins, self.innerjoins)

    def update(self, **values: typing.Any) -> sqlalchemy.Update:
        select_ids = self.queryset.with_only_columns(getattr(self.model, self.pk_field_name)).scalar_subquery()
        return sqlalchemy.update(self.model).where(getattr(self.model, self.pk_field_name).in_(select_ids)).values(**values)
    
    def exists(self) -> sqlalchemy.Select[tuple[bool]]:
        return sqlalchemy.select(sqlalchemy.exists(self.queryset))
    
    def count(self) -> sqlalchemy.Select[tuple[int]]:
        subq = self.queryset.subquery()
        pk_col = getattr(subq.c, self.pk_field_name) 
        return sqlalchemy.select(sqlalchemy.func.count(sqlalchemy.func.distinct(pk_col)))
    
    def delete(self) -> sqlalchemy.Delete[Model]:
        select_ids = self.queryset.with_only_columns(getattr(self.model, self.pk_field_name)).scalar_subquery()
        return sqlalchemy.delete(self.model).where(getattr(self.model, self.pk_field_name).in_(select_ids))
    
    def all(self) -> typing.Self:
        return self


__all__ = ("BaseRepository", "queryset_builder")
