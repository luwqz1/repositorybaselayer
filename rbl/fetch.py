from rbl.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fntypes import Option, Some, Nothing
import sqlalchemy


async def fetch_one[DataModel, *Ts](
    session: AsyncSession,
    repository: BaseRepository[DataModel, *Ts]
) -> Option[DataModel]:
    result = await session.execute(repository.queryset)
    row = result.unique().first()
    if row is None:
        return Nothing()
    return Some(repository.bind(*row))  # type: ignore


async def fetch_many[DataModel, *Ts](
    session: AsyncSession,
    repository: BaseRepository[DataModel, *Ts]
) -> list[DataModel]:
    result = await session.execute(repository.queryset)
    rows = result.unique().all()
    return list([repository.bind(*row) for row in rows])  # type: ignore


async def fetch_scalar[Scalar](
    session: AsyncSession,
    queryset: sqlalchemy.Select[tuple[Scalar]],
) -> Scalar:
    result = await session.execute(queryset)
    row = result.unique().first()
    assert row is not None
    return row[0]


async def fetch_scalars[Scalar](
    session: AsyncSession,
    queryset: sqlalchemy.Select[tuple[Scalar]],
) -> list[Scalar]:
    result = await session.execute(queryset)
    rows = result.unique().scalars().all()
    return list(rows)
