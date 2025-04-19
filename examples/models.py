import enum
import decimal
import uuid as uuid_lib
from datetime import datetime

from sqlalchemy import Enum, UUID, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKeyMixin:
    uuid: Mapped[uuid_lib.UUID] = mapped_column(UUID(), default_factory=uuid_lib.uuid4, primary_key=True)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


MONEY_FIELD = Numeric(precision=15, scale=2)
Base = object  # FIXME IMPORTME





class ClientMaritalStatus(str, enum.Enum):
    ENGAGED = "ENGAGED"
    SINGLE = "SINGLE"
    DIVORCED = "DIVORCED"


class Client(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    balance: Mapped[decimal.Decimal] = mapped_column(MONEY_FIELD)
    marital_status: Mapped[ClientMaritalStatus] = mapped_column(Enum(ClientMaritalStatus))
