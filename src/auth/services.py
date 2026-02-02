from src.db.models import User
from .schemas import UserCreateModel
from .utils import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import uuid
from datetime import datetime, timezone


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None
    
    async def get_all_users(self, session: AsyncSession):
        result = await session.exec(select(User))
        users = result.scalars().all()
        return users

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        user_dict = user_data.model_dump()
        new_user = User(
            uid=str(uuid.uuid4()),                
            username=user_dict["username"],
            first_name=user_dict.get("first_name"),
            last_name=user_dict.get("last_name"),
            email=user_dict["email"],
            password_hash=generate_password_hash(user_dict["password"]),
            is_verified=user_dict.get("is_verified", False),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user