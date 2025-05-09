from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, String, Column
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    object_id = Column(String)
    image_url = Column(String)
    image_vector = mapped_column(Vector(2560))
