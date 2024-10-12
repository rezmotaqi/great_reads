import json
import uuid
from datetime import datetime, timedelta

import aiofiles
import bcrypt
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext
from starlette import status
from starlette.responses import JSONResponse

from app.core.settings import settings
from app.core.utils import SingletonMeta
from app.handlers.databases import get_mongo_db
from app.repositories.users import UserRepository, get_user_repository
from app.schemas.users import (
	CompleteUserDatabaseOutput,
	LoginInput,
	UserRegistrationInput,
	UserRegistrationOutput,
)


def hash_password(password: str) -> str:
	"""Hashes a password subng bcrypt.

	Args:
					password (str): The password to hash.

	Returns:
					str: The hashed password.
	"""

	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
	return hashed_password.decode("utf-8")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
	def __init__(self, user_repository: UserRepository):
		self.user_repository: UserRepository = user_repository

	async def register_user(
			self, user_registration_input: UserRegistrationInput
	) -> JSONResponse:
		# if not validate_email(user_data.email):
		#     raise HTTPException(status_code=400, detail="Invalid email")
		# if not validate_password(user_data.password):
		#     raise HTTPException(status_code=400, detail="Invalid password")
		# existing_user = await self.user_repository.get_user_by_email(
		# user_data.email) if existing_user: raise HTTPException(
		# status_code=400, detail="User already exists")

		hashed_password = pwd_context.hash(user_registration_input.password)
		await self.user_repository.create_user(
			user_registration_input, hashed_password=hashed_password
		)

		return JSONResponse(
			status_code=status.HTTP_201_CREATED,
			content=UserRegistrationOutput,
		)

	async def login_user(self, user_data: LoginInput):
		user = await self.user_repository.get_user_by_email(user_data.email)
		if not user or not check_password(user_data.password, user.password):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Unauthorized"
			)

		access_token = Jwt.generate(
			user_id=user.id,
			user_permissions=await get_user_repository().get_permissions(
				user_id=user.id
			),
		)
		return access_token


async def get_authentication_service(
		user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
	return AuthService(user_repository=user_repository)


credentials_exception = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Could not validate credentials",
	headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
		token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login")),
		db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
	payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
		settings.ALGORITHM])
	user_id: str = payload.get("sub")

	if user_id is None:
		raise credentials_exception
	user = CompleteUserDatabaseOutput.model_validate(
		{**await UserRepository(db=db).get_user_by_id(
			user_id=ObjectId(user_id))}
	)
	if not user:
		raise credentials_exception
	return user


def check_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


class Jwt:

	@staticmethod
	def decode(token: str):
		try:
			payload = jwt.decode(
				token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
			)
			return payload
		except ExpiredSignatureError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token has expired",
				headers={"WWW-Authenticate": "Bearer"},
			)
		except JWTError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid token",
				headers={"WWW-Authenticate": "Bearer"},
			)

	@staticmethod
	def generate(user_id: ObjectId, user_permissions: list) -> str:
		now = datetime.utcnow()
		token_expire = now + timedelta(
			minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
		jwt_payload = {
			"sub": str(user_id),
			"exp": token_expire,
			"iat": now,
			"jti": str(uuid.uuid4()),
			"permissions": user_permissions,
		}
		access_token = jwt.encode(
			jwt_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
		)
		print(access_token)
		return access_token


class PermissionManager(metaclass=SingletonMeta):

	def __init__(self):
		self.permissions = {}

	async def initialize(self):
		await self.load_permissions()

	async def load_permissions(self):
		try:
			async with aiofiles.open("permissions.json", "r") as f:
				contents = await f.read()
				self.permissions = json.loads(contents)
		except FileNotFoundError as e:
			print("Error: permissions.json not found.")
			self.permissions = {
				"endpoints": {},
				"all_permissions": [],
				"public_endpoints": [],
			}
			await self.save_permissions()
			raise e

	async def get_endpoint_permissions(self, endpoint, method):
		endpoint_permissions: dict = self.permissions["endpoints"].get(
			endpoint)
		if endpoint_permissions:
			return endpoint_permissions.get(method, [])
		return []

	async def edit_permissions(self, endpoint, method, new_permissions: list):
		valid_permissions = self.permissions["all_permissions"]
		for permission in new_permissions:
			if permission not in valid_permissions:
				raise ValueError(f"Invalid permission: {permission}")
		if endpoint not in self.permissions["endpoints"]:
			self.permissions["endpoints"][endpoint] = {}
		self.permissions["endpoints"][endpoint][method] = new_permissions
		await self.save_permissions()

	async def save_permissions(self):

		try:
			async with aiofiles.open("permissions.json", "w") as f:
				await f.write(json.dumps(self.permissions))
		except FileNotFoundError as e:
			print("Error: permissions.json not found.")
			raise e

	async def get_public_endpoints(self):
		return self.permissions["public_endpoints"]


async def get_permission_manager():
	permission_manager = PermissionManager()
	await permission_manager.initialize()
	return permission_manager


class Role:
	def __init__(self, permissions=None):
		self.permissions = permissions or []

	def has_permission(self, permission):
		return permission in self.permissions


class AdminRole(Role):
	def __init__(self):
		super().__init__(
			permissions=["read_users", "create_users", "update_books",
						 "delete_books"]
		)


class ReaderRole(Role):
	def __init__(self):
		super().__init__(permissions=["read_books"])


user_role = AdminRole()
