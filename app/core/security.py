from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError, JWTError
#from jwt import ExpiredSignatureError, InvalidTokenError
from app.core.config import settings

# контекст хеширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _hash_password(password: str) -> str:
    """Хеширует пароль"""
    return pwd_context.hash(password)

def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    """Создает JWT токен"""
    to_encode = data.copy()
    ttl_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    })
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Верифицирует JWT токен"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    
    except ExpiredSignatureError as e:
        raise ValueError("Токен истёк") from e

    except JWTError as e:
        raise ValueError("Некорректный токен") from e
    