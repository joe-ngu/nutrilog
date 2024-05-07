import uuid

from pydantic import BaseModel, ConfigDict, Field

class Food(BaseModel):
    '''Food model'''

    model_config = ConfigDict(from_attributes=True)

    pk: uuid.UUID
    name: str
    quantity: float
    fats: float
    carbs: float
    protein: float

class FoodPayload(BaseModel):
    '''Food payload model'''
    
    name: str = Field(min_length=1, max_lenght=127)
    quantity: float = Field(decimal_places=3)
    fats: float = Field(decimal_places=3)
    carbs: float = Field(decimal_places=3)
    protein: float = Field(decimal_places=3)

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pk:uuid.UUID
    name: str
    foods: list[Food]

class UserPayload(BaseModel):
    '''Potion payload model'''
    name: str = Field(min_length=1, max_length=127)
    foods: list[uuid.UUID] = Field(min_length=1)
