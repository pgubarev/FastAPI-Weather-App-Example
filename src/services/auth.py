import secrets

from sqlalchemy.future import select

from db.models import ConfirmationCode, User

from .base import BaseDataAccessService


class AuthCodesService(BaseDataAccessService):

    async def create_confirmation_code_for_user(self, user: User) -> str:
        code = self._generate_code()

        confirmation_code = ConfirmationCode(email=user.email, code=code)

        self.session.add(confirmation_code)
        await self.session.commit()

        return code

    async def confirm_user_email(self, email, code):
        db_request = select(ConfirmationCode).where(
            ConfirmationCode.email == email,
            ConfirmationCode.code == code,
        ).limit(1)
        results = await self.session.execute(db_request)
        results = results.all()

        if len(results) == 0:
            msg = 'invalid email/confirmation code pair'
            raise self.DataServiceException(msg)

        confirmation_code = results[0][0]

        db_request = select(User).where(User.email == email).limit(1)
        results = await self.session.execute(db_request)
        results = results.all()

        if len(results) == 0:
            msg = 'user not found'
            raise self.DataServiceException(msg)

        user = results[0][0]
        user.is_active = True

        self.session.add(user)

        await self.session.delete(confirmation_code)
        await self.session.commit()

    def _generate_code(self) -> str:
        return ''.join([str(secrets.randbelow(10)) for _ in range(4)])
