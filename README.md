# coolrepo

```python
class ClientRepository(BaseRepository[Client]):
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


def find_boyfriend():
    qs = (
        ClientRepository()
        .marital_status([ClientMaritalStatus.SINGLE, ClientMaritalStatus.DIVORCED])
        .balance_range(1_000_000, None)
        .all()
    )

    all_count = fetch_scalar(qs.count())
    first_page = fetch_many(qs.paginate(page=1, per_page=10))

    print(f"There are {all_count} available boyfriends")
    print("Printing first page:")

    for boyfriend in first_page:
        print(boyfriend)
```
