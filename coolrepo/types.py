import typing

if typing.TYPE_CHECKING:
    from _typeshed import SupportsDunderLE, SupportsDunderGE

type Comparable = SupportsDunderLE[typing.Any] | SupportsDunderGE[typing.Any]
