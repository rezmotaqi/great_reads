from fastapi import HTTPException, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.authentication import Jwt, get_permission_manager


async def auth_middleware(request: Request, call_next):
    try:
        permission_manager = await get_permission_manager()

        # Allow public endpoints without authentication
        if request.url.path in await permission_manager.get_public_endpoints():
            return await call_next(request)

        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        if not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
            )

        # Decode the JWT and get the payload
        payload = Jwt.decode(token=token[len("Bearer ") :].strip())

        # Check if the user is a superuser
        if payload.get("isu"):
            return await call_next(request)

        # Check the required permissions for the endpoint
        required_permissions = await permission_manager.get_endpoint_permissions(
            request.url.path, request.method
        )
        missing_permissions = set(required_permissions) - set(payload.get("prs"))
        if missing_permissions:
            response_text = (
                f"Insufficient permissions. Missing: "
                f"{', '.join(missing_permissions)}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=response_text,
            )

        # If everything checks out, call the next middleware or route handler
        return await call_next(request)

    except HTTPException as exc:
        # Return the HTTPException raised in the flow
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )
