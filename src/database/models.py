from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Index
from sqlmodel import SQLModel, Field, Column


class Contact(SQLModel, table=True):
    __tablename__ = "contacts"

    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, autoincrement=True))
    first_name: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    last_name: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    phone_number: str = Field(
        sa_column=Column(pg.TEXT, nullable=False, unique=True, index=True)
    )
    address: str = Field(sa_column=Column(pg.TEXT, nullable=False))

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow, nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )
    )

    __table_args__ = (Index("idx_first_last_name", "first_name", "last_name"),)

    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name} {self.phone_number} {self.address}>"
