from bson import ObjectId
from fastapi import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.authentication import get_permission_manager, Jwt
from app.core.utils import get_app_state_mongo_db
from app.repositories.users import UserRepository


async def auth_middleware(request: Request, call_next):
    permission_manager = await get_permission_manager()
    if request.url.path in await permission_manager.get_public_endpoints():
        return await call_next(request)
    token = request.headers.get("Authorization")
    if token is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"},
        )

    if not token.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"},
        )

    payload = Jwt.decode(request.headers.get("Authorization"))

    user = await UserRepository(get_app_state_mongo_db()).get_user_by_id(
        user_id=ObjectId(payload.get("sub"))
    )

    required_permissions = await permission_manager.get_endpoint_permissions(
        request.url.path, request.method
    )

    missing_permissions = set(required_permissions) - set(
        user.get("permissions")
    )
    if missing_permissions:
        response_text = (
            f"Insufficient permissions. Missing: "
            f"{', '.join(missing_permissions)}"
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": response_text},
        )

    request.state.user = user

    return await call_next(request)
