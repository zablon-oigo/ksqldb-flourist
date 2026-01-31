from sqlmodel import SQLModel, Field, Relationship, Column 
from typing import Optional, List 
from sqlalchemy import String
from enum import Enum as pyEnum 
import uuid
from datetime import datetime, timezone
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import func, ForeignKey


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(
        sa_column=Column(
            mysql.CHAR(36),
            primary_key=True,
            unique=True,
            nullable=False,
            default=lambda: str(uuid.uuid4())
        )
    )
    username: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False))
    email: str = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False, unique=True, index=True))
    first_name: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), nullable=True))
    last_name: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), nullable=True))
    is_admin: bool = False
    is_verified: bool = Field(sa_column=Column(mysql.BOOLEAN, default=False))
    password_hash: str = Field(sa_column=Column(mysql.VARCHAR(255), nullable=False))
    created_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, default=datetime.now(timezone.utc)))
    updated_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)))

    def __repr__(self):
        return f"<User {self.username}>"
    



class Frequency(str, pyEnum):
    daily="daily"
    weekly="weekly"
    bi_weekly= "bi-weekly"
    monthly= "monthly" 



class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: str = Field(
        sa_column=Column(
            mysql.CHAR(36),
            primary_key=True,
            unique=True,
            nullable=False,
            default=lambda: str(uuid.uuid4())
        )
    )
    user_id: str = Field(
        sa_column=Column(mysql.CHAR(36), ForeignKey("user.id"))
    )
    frequency: Frequency 
    active: bool = True
    next_delivery: datetime
    created_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, default=datetime.now(timezone.utc)))
    updated_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)))
    cancelled_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=True))
    user: User = Relationship(back_populates="subscriptions")


class Bouquet(SQLModel, table=True):
    __tablename__ = "bouquet"

    id: str = Field(
        sa_column=Column(
            mysql.CHAR(36),
            primary_key=True,
            unique=True,
            nullable=False,
            default=lambda: str(uuid.uuid4())
        )
    )
    name: str
    description: str 
    price: float
    subscription_fee: float = 0.0
    image_url: Optional[str] = None 
    is_available: bool =True 
    created_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, default=datetime.now(timezone.utc)))
    subscriptions: List["Subscription"] = Relationship(back_populates="bouquet")
    
    