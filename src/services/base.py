from db import AsyncSession


class BaseDataAccessService:
    class DataServiceException(Exception):
        def __init__(self, detail=None):
            super().__init__(detail)
            self.detail = detail

    def __init__(self, session: AsyncSession):
        self.session = session
