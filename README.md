# coolrepo

```python
class ClientRepository(BaseRepository[Client]):
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

    all_count = await fetch_scalar(session, qs.count())
    first_page = await fetch_many(session, qs.paginate(page=1, per_page=10))

    print(f"There are {all_count} available boyfriends")
    print("Printing first page:")

    for boyfriend in first_page:
        print(boyfriend)
```
