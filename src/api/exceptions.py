from typing import Any, Dict, Optional

from fastapi.exceptions import HTTPException
from starlette import status


class BadRequest(HTTPException):
    def __init__(self, detail: Any = None,
                 headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=detail, headers=headers)
