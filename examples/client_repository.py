from .models import Client, ClientMaritalStatus
from coolrepo import BaseRepository, queryset_builder, range_filter


class ClientRepository(BaseRepository[Client]):
    model = Client

    @queryset_builder
    def marital_status(self, marital_statuses: list[ClientMaritalStatus]):
        return self.queryset.filter(Client.marital_status.in_(marital_statuses))
    
    @queryset_builder
    @range_filter
    def balance_range():
        return Client.balance
    
    @queryset_builder
    @range_filter
    def created_at_range():
        return Client.created_at


async def find_boyfriend():
    qs = (
        ClientRepository()
        .marital_status([ClientMaritalStatus.SINGLE, ClientMaritalStatus.DIVORCED])
        .balance_range(1_000_000, None)
        .all()
    )

    all_count_qs = qs.count()
    first_page_qs = qs.paginate(1, 10).queryset
