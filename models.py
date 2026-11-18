from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class Habit(Base): # By inheriting from Base, we're telling SQLAlchemy: "This Python class represents a database table"
    
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)