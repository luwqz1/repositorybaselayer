from .base import BaseRepository, queryset_builder

from rbl.tools.misc import classproperty
from rbl.tools.magic import get_generic_arguments
from rbl.join import Join, join_all
from rbl.types import Field


import typing
import sqlalchemy


DEFAULT_PK_NAME = "id"
PK = typing.Any  # FIXME


class ModelRepository[Model, DataModel = Model, *Columns = *tuple[Model]](BaseRepository[DataModel, *Columns]):

    outerjoins: tuple[Field[typing.Any] | Join, ...] = ()
    innerjoins: tuple[Field[typing.Any] | Join, ...] = ()

    if typing.TYPE_CHECKING:
        model: type[Model]
        pk: Field[PK]
    else:
        @classproperty
        def model(cls):
            return get_generic_arguments(cls, ModelRepository).unwrap()[0]
        
        @classproperty
        def pk(cls) -> Field[T]:
            return getattr(cls.model, DEFAULT_PK_NAME)

    def __init__(self):
        super().__init__()
        self._queryset = join_all(self._queryset, self.outerjoins, self.innerjoins)

    def bind(self, *columns: *tuple[*Columns]) -> DataModel:  # FIXME 
        return columns[0]  # type: ignore

    def select(self) -> sqlalchemy.Select[tuple[*Columns]]:
        return sqlalchemy.select(cls.model).filter()  # type: ignore

    @queryset_builder
    def paginate(self, page: int, per_page: int) -> sqlalchemy.Select[tuple[*Columns]]:
        return self.queryset.order_by(self.pk).limit(per_page).offset((page - 1) * per_page)

    @queryset_builder
    def get(self, pk: PK) -> sqlalchemy.Select[tuple[*Columns]]:
        return self.queryset.filter(self.pk == pk)
    
    @queryset_builder
    def get_many(self, pks: typing.Sequence[PK]) -> sqlalchemy.Select[tuple[*Columns]]:
        return self.queryset.filter(self.pk.in_(pks))

    def update(self, **values: typing.Any) -> sqlalchemy.Update:
        select_ids = self.queryset.with_only_columns(self.pk).scalar_subquery()
        return sqlalchemy.update(self.model).where(self.pk.in_(select_ids)).values(**values)

    @classmethod
    def create(cls, instance: Model) -> sqlalchemy.Insert:
        return sqlalchemy.insert(cls.model).values(**instance)
    
    def count(self) -> sqlalchemy.Select[tuple[int]]:
        return sqlalchemy.select(sqlalchemy.func.count(sqlalchemy.func.distinct(self.pk)))

    def delete(self) -> sqlalchemy.Delete[Model]:
        select_ids = self.queryset.with_only_columns(self.pk).scalar_subquery()
        return sqlalchemy.delete(self.model).where(self.pk.in_(select_ids))
