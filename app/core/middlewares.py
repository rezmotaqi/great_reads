from fastapi import HTTPException, status
from starlette.requests import Request

from app.core.authentication import Jwt, get_permission_manager
from app.repositories.users import get_user_repository


async def auth_middleware(request: Request, call_next):
    permission_manager = await get_permission_manager()
    if request.url.path in await permission_manager.get_public_endpoints():
        return await call_next(request)

    if request.headers.get("Authorization") is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    payload: dict = await Jwt.decode(request.headers.get("Authorization"))

    user = await get_user_repository().get_user_by_id(payload.get("sub"))

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
