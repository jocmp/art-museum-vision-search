from io import BytesIO
from fastapi import UploadFile
from sqlalchemy import select

from app.db import db_session
from app.image_vector import extract_image_vector
from app.models.embedding import Embedding
from PIL import Image
import base64


async def search_related_images(image: UploadFile):
    contents = await image.read()
    image = Image.open(BytesIO(contents))
    img_io = BytesIO()
    image.save(img_io, "JPEG", optimize=True, quality=75)
    img_io.seek(0)
    image_bytes = img_io.getvalue()
    img = base64.b64encode(image_bytes).decode("utf-8")

    image_vector = extract_image_vector(img)

    with db_session() as session:
        results = session.scalars(select(Embedding).order_by(
            Embedding.image_vector.l2_distance(image_vector)).limit(10))

        return [{
            "object_id": row.object_id,
            "image_url": row.image_url,
        } for row in results]
