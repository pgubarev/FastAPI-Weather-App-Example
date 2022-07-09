from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from .base import Base


class ConfirmationCode(Base):
    __tablename__ = 'confirmation_codes'

    email = Column(String(255), unique=True, nullable=False)
    code = Column(String(4), unique=False, nullable=False)
