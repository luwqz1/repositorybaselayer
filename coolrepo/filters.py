import typing

type Numeric = int | float


def range_filter[R, Field](
    func: typing.Callable[[], Field],
) -> typing.Callable[[R, Numeric | None, Numeric | None], typing.Any]:  # type: ignore
    def wrapper(self: R, gte: Numeric | None = None, lte: Numeric | None = None):  # type: ignore
        field = func()
        qs = getattr(self, "queryset")
        if gte is not None:
            qs = qs.filter(field >= gte)  # type: ignore
        if lte is not None:
            qs = qs.filter(field <= lte)  # type: ignore
        return qs
    return wrapper
