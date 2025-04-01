from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Book(BaseModel):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer)
    pages = Column(Integer)
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="books")