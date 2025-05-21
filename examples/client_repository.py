from examples.models import Client, ClientMaritalStatus

from coolrepo.repository import ModelRepository, queryset_builder
from coolrepo.filters import range_filter


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

    all_count_qs = qs.count()
    first_page_qs = qs.paginate(1, 10).queryset
