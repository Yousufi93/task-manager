from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# ==================== تنظیمات ====================

SECRET_KEY = "your-secret-key-change-this-in-production-please"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ==================== پسورد ====================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """پسورد را هش می‌کند."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """بررسی می‌کند که پسورد خام با هش مطابقت دارد."""
    return pwd_context.verify(plain_password, hashed_password)


# ==================== JWT ====================

def create_access_token(username: str) -> str:
    """یک JWT token برای کاربر می‌سازد."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> str | None:
    """توکن را بررسی می‌کند و username را برمی‌گرداند. اگر معتبر نبود، None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None