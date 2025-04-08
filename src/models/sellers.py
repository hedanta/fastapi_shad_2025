from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import BaseModel


class Seller(BaseModel):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    e_mail = Column(String, unique=True, index=True)
    password = Column(String)
    books = relationship("Book", back_populates="seller", cascade="all, delete-orphan", lazy="joined")
