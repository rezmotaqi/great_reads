from fastapi import HTTPException, status
from starlette.requests import Request

from app.core.authentication import (
    get_permission_manager,
    get_user_jwt_payload_data_from_token,
)
from app.schemas.users import JwtExtractedUser

permission_manager = get_permission_manager()


async def auth_middleware(request: Request, call_next):
    """
    Authorization middleware to enforce access control based on JWT and
    permissions.

    This middleware:

    1. Extracts the JWT token from the Authorization header.
    2. Decodes and validates the token to obtain user information,
    including permissions.
    3. Retrieves the required permissions for the requested endpoint from
    the PermissionManager.
    4. Checks if the user has the necessary permissions to access the
    endpoint. If not, raises an HTTPException with
    a 403 Forbidden status code.

    Args: request (Request): The incoming request. call_next (Callable): The
    next middleware or route handler in the chain.
    """
    if request.url.path in await permission_manager.get_public_endpoints():
        return await call_next(request)
    if request.headers.get("Authorization") is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization header",
        )
    user: JwtExtractedUser = await get_user_jwt_payload_data_from_token(
        request.headers.get("Authorization")
    )
    required_permissions = permission_manager.get_endpoint_permissions(
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
