import uuid

from pydantic import BaseModel, ConfigDict, Field


class Food(BaseModel):
    """Food model"""

    model_config = ConfigDict(from_attributes=True)

    pk: uuid.UUID
    name: str
    quantity: float
    fats: float
    carbs: float
    protein: float


class FoodPayload(BaseModel):
    """Food payload model"""

    name: str = Field(min_length=1, max_length=127)
    quantity: float = Field(ge=0)
    fats: float = Field(ge=0)
    carbs: float = Field(ge=0)
    protein: float = Field(ge=0)


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pk: uuid.UUID
    name: str
    foods: list[Food]


class UserPayload(BaseModel):
    """User payload model"""

    name: str = Field(min_length=1, max_length=127)
    foods: list[uuid.UUID] = Field(min_length=0)
