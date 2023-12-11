from sqlalchemy import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.mysql import LONGBLOB


class Base(DeclarativeBase):
    pass


class Patient(Base):
    __tablename__ = "Patients"

    id_patient: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    address: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    phone: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    document: Mapped[bytes] = mapped_column(LONGBLOB, nullable=False)
