from __future__ import annotations

import typing

from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select


class ABCRepository(ABC):
    @property
    @abstractmethod
    def queryset(self) -> Select[typing.Any]: ...

    @queryset.setter
    @abstractmethod
    def queryset(self, value: Select[typing.Any], /) -> None: ...


__all__ = ("ABCRepository",)
