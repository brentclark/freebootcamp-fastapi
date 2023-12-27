from passlib.context import CryptContext
from typing import Any

pwd_context: Any = CryptContext(schemes=["pbkdf2_sha512"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> Any:
    try: 
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return False