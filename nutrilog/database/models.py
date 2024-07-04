import uuid
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    """Base database model"""

    pk: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


user_food_association = Table(
    "user_food",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.pk")),
    Column("food_id", UUID(as_uuid=True), ForeignKey("food.pk")),
)


class Food(Base):
    """Food database model"""

    __tablename__ = "food"

    name: Mapped[str]
    quantity: Mapped[float]
    fats: Mapped[float]
    carbs: Mapped[float]
    protein: Mapped[float]


class User(Base):
    """Potion database model"""

    __tablename__ = "user"

    name: Mapped[str]
    foods: Mapped[list["Food"]] = relationship(
        secondary=user_food_association, backref="user", lazy="selectin"
    )
