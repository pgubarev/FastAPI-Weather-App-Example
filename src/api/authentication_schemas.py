from fastapi.param_functions import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from starlette import status

from .jwt import decode_jwt


jwt_scheme = HTTPBearer()


async def get_current_user_data(token: str = Depends(jwt_scheme)) -> dict:
    user_info = decode_jwt(token)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token')

    return user_info

current_user_data = Depends(get_current_user_data)
