from sqlalchemy.ext.declarative import declarative_base
from pgvector import Vector
from sqlalchemy import BigInteger, Column
from app.models import Base


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(BigInteger, primary_key=True)
    image_vector = Column(Vector(3))
