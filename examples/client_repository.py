from examples.models import Client, ClientMaritalStatus

from rbl.repository import ModelRepository, queryset_builder
from rbl.filters import range_filter
from rbl.fetch import fetch_scalar, fetch_many

from sqlalchemy.ext.asyncio import AsyncSession


session: AsyncSession  # SET ME


class ClientRepository(ModelRepository[Client]):
    @queryset_builder
    def marital_status(self, marital_statuses: list[ClientMaritalStatus]):
        return self.queryset.filter(Client.marital_status.in_(marital_statuses))

    @queryset_builder
    @range_filter
    def balance_range(self):
        return Client.balance
    
    @queryset_builder
    @range_filter
    def created_at_range(self):
        return Client.created_at


async def find_boyfriend():
    qs = (
        ClientRepository()
        .marital_status([ClientMaritalStatus.SINGLE, ClientMaritalStatus.DIVORCED])
        .balance_range(min=1_000_000)
        .all()
    )

    count = await fetch_scalar(session, qs.count())

    page, per_page = 1, 10

    while page <= (count // per_page):
        if page > 1:
            input("\nPress enter for next page >")
        
        boyfriend_page = await fetch_many(session, qs.paginate(page, per_page))

        print(f"\nThere are {count} available boyfriends")
        print("Printing first page:\n\n---")

        for boyfriend in boyfriend_page:
            print(boyfriend)
        
        print("---\n\n")

        page += 1

    print("All available boyfriends printed.")
