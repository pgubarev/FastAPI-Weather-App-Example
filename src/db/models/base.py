from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True)
