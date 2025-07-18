from datetime import datetime
from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB  # Правильный импорт JSONB
from sqlalchemy import Index

from database.engine import Base

class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связи
    dishes: Mapped[list['Dish']] = relationship(back_populates='restaurant', cascade='all, delete-orphan')
    staff: Mapped[list['User']] = relationship(back_populates='restaurant')
    
    def __repr__(self):
        return f"<Restaurant {self.title}>"

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    tg_username: Mapped[str | None] = mapped_column(String(50), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100))
    is_waiter: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_active: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Связь с рестораном
    restaurant_id: Mapped[int | None] = mapped_column(
        ForeignKey('restaurants.id', ondelete='SET NULL'), 
        index=True,
        nullable=True
    )
    restaurant: Mapped['Restaurant'] = relationship(back_populates='staff')
    
    # Статистика обучения
    total_training_time: Mapped[int] = mapped_column(default=0)  # в минутах
    last_trained_dish: Mapped[int | None] = mapped_column(ForeignKey('dishes.id'), nullable=True)
    
    def __repr__(self):
        return f"<User {self.tg_id} ({self.full_name})>"

class Dish(Base):
    __tablename__ = 'dishes'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    cooking_time: Mapped[int | None] = mapped_column(nullable=True)  # в минутах
    is_available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ингредиенты в JSONB формате
    ingredients: Mapped[list[dict]] = mapped_column(
        JSONB(none_as_null=True), 
        default=list,
        comment="Список ингредиентов в формате [{'name':str, 'amount':float, 'unit':str}]"
    )
    
    # Контент из телеги (Telegram file_id)
    dish_photo_id: Mapped[str] = mapped_column(String(255))
    ingredients_photo_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    audio_guide_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    video_guide_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Связь с рестораном
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey('restaurants.id', ondelete='CASCADE'),
        index=True
    )
    restaurant: Mapped['Restaurant'] = relationship(back_populates='dishes')
    
    def __repr__(self):
        return f"<Dish {self.name} (Restaurant {self.restaurant_id})>"

class TrainingSession(Base):
    __tablename__ = 'training_sessions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    dish_id: Mapped[int | None] = mapped_column(ForeignKey('dishes.id', ondelete='SET NULL'), index=True, nullable=True)
    start_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    end_time: Mapped[datetime | None] = mapped_column(nullable=True)
    score: Mapped[int | None] = mapped_column(nullable=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    user: Mapped['User'] = relationship()
    dish: Mapped['Dish'] = relationship()
    
    @property
    def duration(self) -> float:
        """Длительность тренировки в секундах"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

class Question(Base):
    __tablename__ = 'questions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dish_id: Mapped[int] = mapped_column(ForeignKey('dishes.id', ondelete='CASCADE'), index=True)
    question_text: Mapped[str] = mapped_column(Text)
    options: Mapped[list[str]] = mapped_column(JSONB)
    correct_answer: Mapped[int] = mapped_column()  # индекс правильного ответа
    difficulty: Mapped[int] = mapped_column(default=1)  # 1-легкий, 2-средний, 3-сложный
    
    dish: Mapped['Dish'] = relationship()
