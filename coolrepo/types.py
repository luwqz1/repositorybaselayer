import typing
from sqlalchemy.sql.elements import ColumnElement

if typing.TYPE_CHECKING:
    from _typeshed import SupportsDunderLE, SupportsDunderGE

type Comparable = SupportsDunderLE[typing.Any] | SupportsDunderGE[typing.Any]
type Field[T] = ColumnElement[T]
