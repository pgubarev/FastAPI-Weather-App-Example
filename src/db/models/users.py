from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from .base import Base


class User(Base):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), unique=False, nullable=False)
    last_name = Column(String(255), unique=False, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=False)
    city_id = Column(Integer, ForeignKey("cities.id"))
