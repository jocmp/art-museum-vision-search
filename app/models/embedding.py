from sqlalchemy.ext.declarative import declarative_base
from pgvector import Vector
from sqlalchemy import BigInteger, String, Column
from app.models import Base


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    object_id = Column(String)
    image_url = Column(String)
    image_vector = Column(Vector(3))
