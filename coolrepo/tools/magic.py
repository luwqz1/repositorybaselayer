import types
import typing

from fntypes.tools.unwrapping import unwrapping
from fntypes.option import Nothing, Option, Some

from coolrepo.tools.functional import from_optional


def get_origin_bases(cls: type[typing.Any], /) -> Option[tuple[typing.Any]]:
    """
    Example::

        class A(B[str], C[int], D): ...

        get_origin_bases(A).unwrap()  # (__main__.B[str], __main__.C[int], <class '__main__.D'>)
    """

    return from_optional(cls.__dict__.get("__orig_bases__"))


@unwrapping
def get_generic_arguments(
    cls: type[typing.Any],
    /,
    from_origin_base: type[typing.Any],
) -> Option[tuple[typing.Any, ...]]:
    """
    Example::

        class A(B[str], C[int], D): ...

        get_generic_arguments(A, from_origin_base=C).unwrap()  # (<class 'int'>,)
    """

    for base in get_origin_bases(cls).unwrap():
        if (typing.get_origin(base) or base) is from_origin_base:
            return Some(typing.get_args(base))

    return Nothing()


@unwrapping
def get_map_generic_arguments(
    cls: type[typing.Any],
    /,
) -> Option[dict[type[typing.Any], tuple[typing.Any, ...]]]:
    """
    Example::

        class A(B[str], C[int], D): ...

        get_map_generic_arguments(A).unwrap()  # {<class '__main__.B'>: (<class 'str'>,), <class '__main__.C'>: (<class 'int'>,)}
    """

    return Some(
        {
            base.__origin__: typing.get_args(base)
            for base in get_origin_bases(cls).unwrap()
            if isinstance(base, types.GenericAlias | typing._GenericAlias)  # type: ignore
            and isinstance(base.__origin__, type)
        },
    )


__all__ = ("get_map_generic_arguments", "get_generic_arguments", "get_origin_bases")
