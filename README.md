# RBL - repository base layer

This library is designed to help you build beautiful repository classes for SQLAlchemy-based projects.

With this instrument you can create convenient repository classes that support changing your query with self-implemented filters that will be applied in a builder style.

```python
qs = UserRepository().has_permission("admin").online_at(min=now() - timedelta(minutes=30))
```

The utility is scalable enough to work on top of any kind of select statement. Supported stack is meant to be expanded in the future.

## What RBL offers

* `ModelRepository` - the base class to easily apply eager joins when selecting from a specific model
* `BaseRepository` - the base class that can rest on top of any base select expression that you have to provide manually
* A set of useful filter constructors that really help you to save a big bit of time

## Example

```python
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

    all_count = await fetch_scalar(session, qs.count())
    first_page = await fetch_many(session, qs.paginate(page=1, per_page=10))

    print(f"There are {all_count} available boyfriends")
    print("Printing first page:")

    for boyfriend in first_page:
        print(boyfriend)
```

## Docs

Soon. For now see [examples](/examples/)

