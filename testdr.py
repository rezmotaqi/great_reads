from jose import jwt

from app.core.settings import settings

t = jwt.encode({"test": 1}, "123", algorithm="HS256")


decoded_token = jwt.decode(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzBhNWVjZDE5ZGMzOTNiZTJhYWZhNTciLCJleHAiOjE3Mjg4NDk1MTQsImlhdCI6MTcyODc4OTUxNCwianRpIjoiODg4MGIzZmQtNjIyYy00OTFjLWIzNmYtODBiNDk2N2JiZDkyIiwicHJzIjoiW1wicmVhZHNfYm9va3NcIl0ifQ.ougnyZ3GH4f0sqwwveX66wHDkNmFOyQZxHw5ygyJFpo",
    "123",
    algorithms=settings.ALGORITHM,
)
print(decoded_token)
