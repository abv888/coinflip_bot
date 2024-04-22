from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    full_name = Column('fullname', String)
    username = Column('username', String)
    telegram_id = Column('telegram_id', Integer)
    casino_id = Column('casino_id', Integer)

