from .base import BaseRepository, queryset_builder

from coolrepo.tools.misc import classproperty
from coolrepo.tools.magic import get_generic_arguments
from coolrepo.join import Join, join_all


import typing
import sqlalchemy


class ModelRepository[Model, DataModel = Model, *Columns = *tuple[Model]](BaseRepository[DataModel, *Columns]):
    pk_field_name: str = "uuid"

    outerjoins: tuple[typing.Any | Join, ...] = ()
    innerjoins: tuple[typing.Any | Join, ...] = ()

    if typing.TYPE_CHECKING:
        model: type[Model]
    else:
        @classproperty
        def model(cls):
            return get_generic_arguments(cls, ModelRepository).unwrap()[0]
    
    def __init__(self):
        super().__init__()
        self._queryset = join_all(self._queryset, self.outerjoins, self.innerjoins)

    def bind(self, *columns: *tuple[*Columns]) -> DataModel:  # FIXME 
        return columns[0]  # type: ignore

    def select(self) -> sqlalchemy.Select[tuple[*Columns]]:
        return sqlalchemy.select(cls.model).filter()  # type: ignore

    @queryset_builder
    def paginate(self, page: int, per_page: int) -> sqlalchemy.Select[tuple[*Columns]]:
        return self.queryset.order_by(self.pk_field.asc()).limit(per_page).offset((page - 1) * per_page)

    @queryset_builder
    def get(self, uuid: str) -> sqlalchemy.Select[tuple[*Columns]]:
        return self.queryset.filter(self.pk_field == uuid)

    def update(self, **values: typing.Any) -> sqlalchemy.Update:
        select_ids = self.queryset.with_only_columns(self.pk_field).scalar_subquery()
        return sqlalchemy.update(self.model).where(self.pk_field.in_(select_ids)).values(**values)

    @classmethod
    def create(cls, instance: Model) -> sqlalchemy.Insert:
        return sqlalchemy.insert(cls.model).values(**instance)
    
    def count(self) -> sqlalchemy.Select[tuple[int]]:
        subq = self.queryset.subquery()
        pk_col = getattr(subq.c, self.pk_field_name) 
        return sqlalchemy.select(sqlalchemy.func.count(sqlalchemy.func.distinct(pk_col)))

    def delete(self) -> sqlalchemy.Delete[Model]:
        select_ids = self.queryset.with_only_columns(self.pk_field).scalar_subquery()
        return sqlalchemy.delete(self.model).where(self.pk_field.in_(select_ids))
    
    @classproperty
    def pk_field(cls):
        return getattr(cls.model, cls.pk_field_name)
