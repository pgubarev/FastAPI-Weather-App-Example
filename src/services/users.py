import hashlib
from typing import Optional

from sqlalchemy.future import select

from conf import settings
from db.models import User

from .base import BaseDataAccessService


class UsersService(BaseDataAccessService):

    async def is_user_exists(self, email: str) -> bool:
        db_request = select(User.id).where(User.email == email).limit(1)
        results = await self.session.execute(db_request)
        return len(results.all()) == 1

    async def create_new_user(self, commit: bool = True,
                              **kwargs: dict) -> User:
        password_hash = self._generate_password_hash(kwargs.pop('password'))

        user = User(password=password_hash, **kwargs)

        self.session.add(user)
        if commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        password_hash = self._generate_password_hash(password)
        db_request = select(User).where(
            User.email == email, User.password == password_hash,
            User.is_active == True,
        ).limit(1)
        results = await self.session.execute(db_request)
        results = results.all()

        return results[0][0] if results else None

    @classmethod
    def _generate_password_hash(cls, raw_password) -> str:
        value = (raw_password + settings.SECRET_KEY).encode()
        return hashlib.sha512(value).hexdigest()

    def _check_password(self, raw_password, user: User) -> bool:
        password = self._generate_password_hash(raw_password)
        return password == user.password
