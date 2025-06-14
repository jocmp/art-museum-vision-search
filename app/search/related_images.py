from PIL import Image
import io
from fastapi import UploadFile
from sqlalchemy import select

from app.db import db_session
from app.image_vector import extract_image_vector
from app.models.embedding import Embedding


async def search_related_images(image: UploadFile):
    contents = await image.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    image_vector = extract_image_vector(img)

    with db_session() as session:
        results = session.scalars(select(Embedding).order_by(
            Embedding.image_vector.l2_distance(image_vector)).limit(20))

        return [{
            "object_id": row.object_id,
            "image_url": row.image_url,
        } for row in results]
