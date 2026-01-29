from sqlmodel import SQLModel, Field, Relationship, Column 
from typing import Optional, List 
from sqlalchemy import String
from enum import Enum as pyEnum 
from uuid import UUID, uuid4 
from datetime import datetime 



class Frequency(str, pyEnum):
    daily="daily"
    weekly="weekly"
    bi_weekly= "bi-weekly"
    monthly= "monthly"