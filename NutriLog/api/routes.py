import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from NutriLog.api import models
from NutriLog.api.dependencies import get_repository
from NutriLog.database import models as db_models
from NutriLog.database.repository import DatabaseRepository

router = APIRouter(prefix="/v1", tags=["v1"])

FoodRepository = Annotated[
    DatabaseRepository[db_models.Food], Depends(get_repository(db_models.Food))
]
UserRepository = Annotated[
    DatabaseRepository[db_models.User], Depends(get_repository(db_models.User))
]


@router.post("/food", status_code=status.HTTP_201_CREATED)
async def create_food(
    data: models.FoodPayload, repository: FoodRepository
) -> models.Food:
    food = await repository.create(data.model_dump())
    return models.Food.model_validate(food)


@router.get("/foods", status_code=status.HTTP_200_OK)
async def get_foods(repository: FoodRepository) -> list[models.Food]:
    foods = await repository.filter()
    return [models.Food.model_validate(food) for food in foods]


@router.get("/foods/{pk}", status_code=status.HTTP_200_OK)
async def get_food(pk: uuid.UUID, repository: FoodRepository) -> models.Food:
    food = await repository.get(pk)
    if food is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food does not exist",
        )
    return models.Food.model_validate(food)


@router.gget("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    data: models.User,
    food_repository: FoodRepository,
    user_repository: UserRepository,
) -> models.User:
    data_dict = data.model_dump()
    foods = await food_repository.filter(db_models.Food.pk.in_(data_dict.pop("foods")))
    user = await user_repository.create({**data_dict, "foods": foods})
    return models.User.model_validate(user)


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(repository: UserRepository) -> list[models.User]:
    users = await repository.filter()
    return [models.User.model_validate(user) for user in users]


@router.get("/user/{pk}", status_code=status.HTTP_200_OK)
async def get_user(pk: uuid.UUID, repository: UserRepository) -> models.User:
    user = await repository.get(pk)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return models.User.model_validate(user)
