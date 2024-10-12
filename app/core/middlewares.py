from fastapi import status
from starlette.requests import Request, HTTPException

from app.core.authentication import Jwt, get_permission_manager
from app.core.utils import get_app_state_mongo_db
from app.repositories.users import UserRepository


async def auth_middleware(request: Request, call_next):
    permission_manager = await get_permission_manager()
    if request.url.path in await permission_manager.get_public_endpoints():
        return await call_next(request)

    if request.headers.get("Authorization") is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    token = request.headers.get("Authorization").lstrip("Bearer ")

    payload: dict = await Jwt.decode(
        "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzBhNmJlNzQ3NDg0MzllMDJmYjVmMmUiLCJleHAiOjE3Mjg4MDE2MjUsImlhdCI6MTcyODc0MTYyNSwianRpIjoiYTY3MGIxNjctNDhhZi00ZWY4LWI1NjctY2QwMjVmOGU5MmYwIiwicHJzIjoiW1wicmVhZHNfYm9va3NcIl0ifQ.fxu6gcq06ikQlM2GmHq93eLFWqk-LKIoC9mo7TL3Xqk"
    )

    user = await UserRepository(await get_app_state_mongo_db()).get_user_by_id(
        payload.get("sub")
    )

    required_permissions = await permission_manager.get_endpoint_permissions(
        request.url.path, request.method
    )
    missing_permissions = set(required_permissions) - set(user.permissions)
    if missing_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Missing: "
            f"{', '.join(missing_permissions)}",
        )

    request.state.user = user

    response = await call_next(request)
    return response
