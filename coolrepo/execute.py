from sqlalchemy import Insert, Update, Delete
from sqlalchemy.ext.asyncio import AsyncSession
import typing

Statement = Insert | Update | Delete


@typing.overload
async def execute(session: AsyncSession, statement: Statement) -> typing.Sequence[typing.Any]:
    ...

@typing.overload
async def execute(session: AsyncSession, statement: Statement, *, do_return: typing.Literal[False] = False) -> None:
    ...

async def execute(session: AsyncSession, statement: Statement, do_return: bool = False) -> typing.Sequence[typing.Any] | None:
    result = await session.execute(statement)
    await session.commit()
    if do_return:
        return result.scalars().all()
