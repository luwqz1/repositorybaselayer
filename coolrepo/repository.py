import abc
import typing
import sqlalchemy


Model = typing.TypeVar("Model")
P = typing.ParamSpec("P")
T = typing.TypeVar("T")
Ts = typing.TypeVarTuple("Ts")


def queryset_builder(
    func: typing.Callable[typing.Concatenate[T, P], sqlalchemy.Select[tuple[*Ts]]],
) -> typing.Callable[typing.Concatenate[T, P], T]:
    def wrapper(self: T, *args: P.args, **kwargs: P.kwargs):
        if not hasattr(self, "queryset"):
            raise RuntimeError(
                f"Cannot build query. Queryset is undefined in {self.__class__} repository"
            )
        queryset = func(self, *args, **kwargs)
        setattr(self, "queryset", queryset)
        return self

    return wrapper


class BaseRepository[Model, DataModel = Model, *Selectable = *tuple[Model]](abc.ABC):
    model: type[Model]
    pk_field_name: str = "uuid"

    def __init__(self):
        self.queryset = self.select()

    @classmethod
    def bind(cls, row: tuple[*Selectable]) -> DataModel:
        dct = {}
        for i, column in enumerate(sqlalchemy.inspect(cls.model).c):  # type: ignore
            dct[column.name] = row[i]
        return cls.model(**dct)  # type: ignore

    @classmethod
    def select(cls) -> sqlalchemy.Select[tuple[*Selectable]]:
        return sqlalchemy.select(cls.model).filter()  # type: ignore
    
    @queryset_builder
    def paginate(self, page: int, per_page: int) -> sqlalchemy.Select[tuple[*Selectable]]:
        return self.queryset.limit(per_page).offset((page - 1) * per_page)

    @queryset_builder
    def get(self, uuid: str) -> sqlalchemy.Select[tuple[*Selectable]]:
        return self.queryset.filter(getattr(self.model, self.pk_field_name) == uuid)
    
    @classmethod
    def create(cls, instance: Model) -> sqlalchemy.Insert:
        return sqlalchemy.insert(cls.model).values(**instance)

    def update(self, **values: typing.Any) -> sqlalchemy.Update:
        select_ids = self.queryset.with_only_columns(getattr(self.model, self.pk_field_name)).scalar_subquery()
        return sqlalchemy.update(self.model).where(getattr(self.model, self.pk_field_name).in_(select_ids)).values(**values)
    
    def exists(self) -> sqlalchemy.Select[tuple[bool]]:
        return sqlalchemy.select(sqlalchemy.exists(self.queryset))
    
    def count(self) -> sqlalchemy.Select[tuple[int]]:
        return self.queryset.with_only_columns(sqlalchemy.func.count())
    
    def all(self) -> typing.Self:
        return self
