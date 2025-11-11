from datetime import timedelta, datetime, timezone
from uuid import UUID

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import jwt
import pyotp
from fastapi import HTTPException, Response, status
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from src.config import (
    db_session,
    DEBUG,
    SECRET_KEY,
    TOKEN_EXPIRE,
    ALGORITHM,
    APP_TITLE,
    TOKEN_KEY,
    REFRESH_TOKEN_EXPIRE,
    MAIL_API_KEY,
    MAIL_SENDER,
)
from src.schemes.user import UserScheme, RegisterScheme
from src.models import UserModel

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify user password"""

    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashing user password"""

    return password_hash.hash(password)


def create_token(user_id: UUID, expire: float = TOKEN_EXPIRE) -> str:
    """Create JWT-token"""

    expire = datetime.now(timezone.utc) + timedelta(seconds=expire)
    return jwt.encode(
        {"id": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
    )


def decode_token(token: str) -> UUID:
    """Decode user data"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return UUID(payload.get("id"))
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc


async def create_user(user: RegisterScheme) -> UserModel:
    """Create user instance"""

    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])

    async with db_session() as session:
        stmt = insert(UserModel).values(**user_dict).returning(UserModel)
        try:
            result = await session.execute(stmt)
            await session.commit()
            user_instance = result.scalar()
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            ) from exc

    return user_instance


async def get_user(user_id: UUID) -> UserModel:
    """Get user instance"""

    async with db_session() as session:
        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id)
            .where(UserModel.is_active)
        )
        user = await session.scalar(stmt)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )

    return user


async def user_login(email: str, password: str) -> UserModel:
    """Login user"""

    async with db_session() as session:
        stmt = (
            select(UserModel)
            .where(UserModel.email == email)
            .where(UserModel.is_active)
        )
        user = await session.scalar(stmt)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return user


def set_auth_cookie(response: Response, user_id: UUID) -> None:
    """Set secure auth cookie"""

    token = create_token(user_id, TOKEN_EXPIRE)
    refresh_token = create_token(user_id, REFRESH_TOKEN_EXPIRE)

    response.set_cookie(
        key=TOKEN_KEY,
        value=token,
        httponly=True,
        max_age=TOKEN_EXPIRE,
        samesite="lax",
        secure=DEBUG,
    )
    response.set_cookie(
        key=f"{TOKEN_KEY}_refresh",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE,
        samesite="lax",
        secure=DEBUG,
    )


def refresh_auth_cookie(response: Response, user_id: UUID) -> None:
    """Refresh auth cookie"""

    token = create_token(user_id, TOKEN_EXPIRE)
    refresh_token = create_token(user_id, REFRESH_TOKEN_EXPIRE)

    response.set_cookie(
        key=TOKEN_KEY,
        value=token,
        httponly=True,
        max_age=TOKEN_EXPIRE,
        samesite="lax",
        secure=DEBUG,
    )
    response.set_cookie(
        key=f"{TOKEN_KEY}_refresh",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE,
        samesite="lax",
        secure=DEBUG,
    )


def delete_auth_cookie(response: Response) -> None:
    """Delete auth cookie"""

    response.delete_cookie(key=TOKEN_KEY)
    response.delete_cookie(key=f"{TOKEN_KEY}_refresh")


async def enable_2fa(user_id: UUID) -> str:
    """Enable 2FA for user"""

    async with db_session() as session:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(is_2fa_enabled=True, otp_secret=pyotp.random_base32())
        )
        result = await session.execute(stmt)
        await session.commit()
        user: UserModel = result.scalar_one()

    totp = pyotp.TOTP(user.otp_secret)
    otp_uri = totp.provisioning_uri(name=user.email, issuer_name=APP_TITLE)

    return otp_uri


async def validate_2fa(user_id: UUID, code: str) -> UserModel:
    """Verify 2FA code"""

    user = await get_user(user_id)
    if not user.is_2fa_enabled or not user.otp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is not enabled"
        )

    totp = pyotp.TOTP(user.otp_secret)
    if not totp.verify(code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid 2FA code"
        )

    return user


async def search_users(email_contains: str) -> list[UserModel]:
    """Search users by email substring"""

    async with db_session() as session:
        stmt = (
            select(UserModel)
            .where(UserModel.email.contains(email_contains))
            .where(UserModel.is_active)
        )
        result = await session.scalars(stmt)
        return result.all()


async def update_user(
    user_id: UUID,
    user: UserScheme,
) -> UserModel:
    """Update user information"""

    async with db_session() as session:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user.model_dump())
            .returning(UserModel)
        )

        result = await session.execute(stmt)
        await session.commit()
        user_instance = result.scalar()

    return user_instance


async def delete_user(user_id: UUID) -> None:
    """Soft delete user"""

    async with db_session() as session:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(is_active=False)
        )
        session.execute(stmt)
        await session.commit()


async def reset_password(
    user_id: UUID, old: str, new: str
) -> None:
    """Reset user password"""

    user_model = await get_user(user_id)
    if not verify_password(old, user_model.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )

    async with db_session() as session:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(password=get_password_hash(new))
        )
        await session.execute(stmt)
        await session.commit()


async def forgot_password(email: str, redirect_url: str) -> None:
    """Send mail to user for new password"""

    async with db_session() as session:
        stmt = (
            select(UserModel)
            .where(UserModel.email == email)
            .where(UserModel.is_active)
        )
        user_model = await session.scalar(stmt)

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email",
        )

    send_mail(user_model, redirect_url)


def send_mail(user: UserModel, redirect_url: str) -> None:
    """Send mail to user"""

    token = create_token(user.id)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Chat: Forgot password"
    message["From"] = MAIL_SENDER
    message["To"] = user.email

    text = f"Link to new password: {redirect_url}?token={token}"
    message.attach(MIMEText(text, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(MAIL_SENDER, MAIL_API_KEY)
        server.send_message(message)
