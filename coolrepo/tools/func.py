import typing


class classproperty[R]:
    def __init__(self, fget: typing.Callable[[type[typing.Any]], R]) -> None:
        self.fget = fget

    def __get__(self, instance: typing.Any, owner: type[typing.Any]) -> R:
        return self.fget(owner)


__all__ = ("classproperty",)
