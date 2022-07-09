from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Float

from .base import Base


class City(Base):
    __tablename__ = 'cities'

    name = Column(String(255), unique=True, nullable=False)
    country_code = Column(String(8), unique=False, nullable=False)
    lat = Column(Float(), unique=False, nullable=False)
    lon = Column(Float(), unique=False, nullable=False)
