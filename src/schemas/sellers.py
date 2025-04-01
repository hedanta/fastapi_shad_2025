from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from pydantic_core import PydanticCustomError

from src.schemas.books import ReturnedBook

__all__ = ["SellerBase", "SellerCreate", "SellerUpdate", "Seller"]


class SellerBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    e_mail: EmailStr = Field(..., min_length=1)


class SellerCreate(SellerBase):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise PydanticCustomError(
                "password_length_error",
                "Password must be at least 8 characters long"
            )

        if not any(char.isdigit() for char in value):
            raise PydanticCustomError(
                "password_digit_error",
                "Password must contain at least one digit"
            )

        if not any(char.isupper() for char in value):
            raise PydanticCustomError(
                "password_uppercase_error",
                "Password must contain at least one uppercase letter"
            )

        return value


class SellerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    e_mail: Optional[EmailStr] = Field(None, min_length=1)
    password: Optional[str] = Field(None, min_length=8)


class Seller(SellerBase):
    id: int
    first_name: str
    last_name: str
    e_mail: str
    books: List[ReturnedBook] = []

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)