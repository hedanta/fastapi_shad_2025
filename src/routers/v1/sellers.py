from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List, Annotated

from src.models.sellers import Seller
from src.schemas.sellers import SellerCreate, SellerUpdate, Seller as SellerSchema
from src.configurations import get_async_session

seller_router = APIRouter(tags=["sellers"], prefix="/sellers")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@seller_router.post("/", response_model=SellerSchema, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: SellerCreate, session: DBSession):
    result = await session.execute(
        select(Seller)
        .filter(Seller.e_mail == seller.e_mail)
    )
    db_seller = result.scalars().first()

    if db_seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail already registered"
        )

    new_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        e_mail=seller.e_mail,
        password=seller.password
    )

    session.add(new_seller)
    await session.commit()
    await session.refresh(new_seller)

    return new_seller


@seller_router.get("/", response_model=List[SellerSchema])
async def read_sellers(session: DBSession):
    result = await session.execute(
        select(Seller)
        .options(joinedload(Seller.books))
    )

    return result.unique().scalars().all()


@seller_router.get("/{seller_id}", response_model=SellerSchema)
async def read_seller(seller_id: int, session: DBSession):
    result = await session.execute(
        select(Seller)
        .options(joinedload(Seller.books))
        .where(Seller.id == seller_id)
    )

    seller = result.unique().scalars().first()

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )

    return seller


@seller_router.put("/{seller_id}", response_model=SellerSchema)
async def update_seller(seller_id: int, seller: SellerUpdate, session: DBSession):
    db_seller = await session.execute(
        select(Seller)
        .options(joinedload(Seller.books))
        .where(Seller.id == seller_id)
    )
    db_seller = db_seller.scalars().first()

    if not db_seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )

    for key, value in seller.model_dump(exclude_unset=True).items():
        setattr(db_seller, key, value)

    await session.commit()
    await session.refresh(db_seller)

    return db_seller


@seller_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    db_seller = await session.get(Seller, seller_id)

    if not db_seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )

    await session.delete(db_seller)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
