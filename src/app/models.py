from sqlalchemy import String, Text, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    articles: Mapped[list['Article']] = relationship('Article', back_populates='category')

class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    category: Mapped['Category'] = relationship('Category', back_populates='articles')
    images: Mapped[list['Image']] = relationship('Image', back_populates='article', foreign_keys='Image.article_id')

class Image(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(512), nullable=False)
    hash: Mapped[str] = mapped_column(String(512), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    article_id: Mapped[Optional[int]] = mapped_column(ForeignKey('articles.id'), nullable=True)

    article: Mapped[Optional['Article']] = relationship('Article', back_populates='images', foreign_keys=[article_id])








# class DeletedArticle(Base):
#     __tablename__ = 'deleted_articles'

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     article_id: Mapped[int] = mapped_column(unique=True, nullable=False)
#     title: Mapped[str] = mapped_column(String(255), nullable=False)
#     text: Mapped[str] = mapped_column(Text, nullable=False)
#     category_id: Mapped[int] = mapped_column(nullable=False)
#     key: Mapped[str] = mapped_column(String(512), nullable=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)