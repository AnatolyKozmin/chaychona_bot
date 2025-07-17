from sqlalchemy import Column, BigInteger, Boolean, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.engine import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(String)
    from_rest: Mapped[int]


class Restoraunt(Base):
    __tablename__ = 'restoraunt'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)



class Dishes(Base):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    