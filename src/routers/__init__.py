from fastapi import APIRouter
from .v1 import books, sellers

router = APIRouter()
router.include_router(books.books_router, prefix="/api/v1", tags=["books"])
router.include_router(sellers.seller_router, prefix="/api/v1", tags=["sellers"])