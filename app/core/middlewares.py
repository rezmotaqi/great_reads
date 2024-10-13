from bson import ObjectId
from fastapi import status, HTTPException
from jose import jwt
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.authentication import Jwt, get_permission_manager
from app.core.settings import settings
from app.core.utils import get_app_state_mongo_db
from app.repositories.users import UserRepository


async def auth_middleware(request: Request, call_next):
    permission_manager = await get_permission_manager()
    if request.url.path in await permission_manager.get_public_endpoints():
        return await call_next(request)

    if request.headers.get("Authorization") is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"},
        )

    token = request.headers.get("Authorization").lstrip("Bearer ")

    # payload: dict = await Jwt.decode(token=token)
    # print(payload)

    # decoded_token = jwt.decode(token, "123", algorithms=settings.ALGORITHM)
    # print(decoded_token)
    #
    # decoded_token = jwt.decode(
    #     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzBhNWVjZDE5ZGMzOTNiZTJhYWZhNTciLCJleHAiOjE3Mjg4NDk1MTQsImlhdCI6MTcyODc4OTUxNCwianRpIjoiODg4MGIzZmQtNjIyYy00OTFjLWIzNmYtODBiNDk2N2JiZDkyIiwicHJzIjoiW1wicmVhZHNfYm9va3NcIl0ifQ.ougnyZ3GH4f0sqwwveX66wHDkNmFOyQZxHw5ygyJFpo",
    #     "123",
    #     algorithms=settings.ALGORITHM,
    # )

    decoded_token = jwt.decode(
        # token=token,
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzBiN2I2N2RkMDcyNjAxODY2ODg4YzciLCJleHAiOjE3Mjg4NjU3OTIsImlhdCI6MTcyODgwNTc5MiwianRpIjoiODU2MThlYzEtYzc3NC00Y2Y0LWJlM2ItNWYzYzI2MWNjM2U2IiwicHJzIjpbInJlYWRfYm9va3MiXX0.ecnNkN0XMXwOJOzkepOvUrWT9uovqZcL3csRYZKS78c",
        key="123",
        algorithms=settings.ALGORITHM,
    )

    print(decoded_token)

    user = await UserRepository(get_app_state_mongo_db()).get_user_by_id(
        user_id=ObjectId(decoded_token.get("sub"))
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
