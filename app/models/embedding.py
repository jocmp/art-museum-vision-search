from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, DateTime, String, Column
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    object_id = Column(String)
    image_url = Column(String)
    image_vector = mapped_column(Vector(512))
    updated_at = Column(DateTime(timezone=True))
