from datetime import timedelta, datetime, timezone

import jwt
import pyotp
from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from src.config import SECRET_KEY, TOKEN_EXPIRE, ALGORITHM, APP_TITLE, TOKEN_KEY
from src.schemes.user import UserScheme, LoginScheme, OTPValidateScheme
from src.models import UserModel

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify user password"""

    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashing user password"""

    return password_hash.hash(password)


def create_token(username: str) -> str:
    """Create JWT-token"""

    expire = datetime.now(timezone.utc) + timedelta(seconds=TOKEN_EXPIRE)
    return jwt.encode(
        {"username": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
    )


def decode_token(token: str) -> str:
    """Decode user data"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("username")
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc


async def create_user(session: AsyncSession, user: UserScheme) -> UserModel:
    """Create user instance"""

    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    user = UserModel(**user_dict)

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from exc

    return user


async def get_user(session: AsyncSession, username: str) -> UserModel:
    """Get user instance"""

    stmt = (
        select(UserModel)
        .where(UserModel.username == username)
        .where(UserModel.is_active == True)
    )
    user = await session.scalar(stmt)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )

    return user


async def user_login(
    session: AsyncSession, credentials: LoginScheme
) -> UserModel:
    """Login user"""

    user = await get_user(session, credentials.username)
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return user


def set_auth_cookie(response: Response, username: str) -> None:
    """Set secure auth cookie"""

    token = create_token(username)
    response.set_cookie(
        key=TOKEN_KEY,
        value=token,
        httponly=True,
        max_age=TOKEN_EXPIRE,
        samesite="lax",
        secure=False,  # TODO: Set to True in production
    )


async def enable_2fa(session: AsyncSession, username: str) -> str:
    """Enable 2FA for user"""

    user = await get_user(session, username)
    user.is_2fa_enabled = True
    user.otp_secret = pyotp.random_base32()
    session.add(user)
    await session.commit()
    await session.refresh(user)

    totp = pyotp.TOTP(user.otp_secret)
    otp_uri = totp.provisioning_uri(name=username, issuer_name=APP_TITLE)

    return otp_uri


async def validate_2fa(
    session: AsyncSession, verification: OTPValidateScheme
) -> UserModel:
    """Verify 2FA code"""

    user = await get_user(session, verification.username)
    if not user.is_2fa_enabled or not user.otp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is not enabled"
        )

    totp = pyotp.TOTP(user.otp_secret)
    if not totp.verify(verification.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid 2FA code"
        )

    return user
