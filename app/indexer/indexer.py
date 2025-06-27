import os
import requests
import json
from PIL import Image
from io import BytesIO
from sqlalchemy import select

from app.db import db_session
from app.image_vector import extract_image_vector, init_models
from app.models.embedding import Embedding
from datetime import datetime, timedelta, timezone


def index_images():
    init_models()

    modification_range = generate_modification_range()
    base_collection_url = os.environ.get("ART_MUSEUM_COLLECTION_URL")
    limit = 50
    start = 0

    while True:
        collection_url = f"{base_collection_url}/objectSearch?q=modified:\"{modification_range}\"&limit={limit}&start={start}"

        if not index_batch(collection_url=collection_url):
            print(f"Stopping: limit={limit}, start={start}")
            break

        start += limit


def index_batch(collection_url: str) -> bool:
    try:
        response = requests.get(collection_url)
        response.raise_for_status()

        data = response.json()

        filtered_data = {k: v for k, v in data.items() if k.isdigit()}

        if not filtered_data:
            return False

        for _, art_object in filtered_data.items():
            if "media_large_url" in art_object:
                try:
                    with db_session() as session:
                        existing_embedding = session.scalar(
                            select(Embedding).where(
                                Embedding.object_id == str(
                                    art_object["object_id"])
                            )
                        )

                        if (existing_embedding and existing_embedding.image_url == art_object["media_large_url"]):
                            print(
                                f"Skipping {art_object['object_id']} - already exists")
                            continue

                        img_response = requests.get(
                            art_object["media_large_url"])
                        img_response.raise_for_status()

                        image = Image.open(BytesIO(img_response.content))
                        image_vector = extract_image_vector(image)

                        if existing_embedding:
                            existing_embedding.image_url = art_object["media_large_url"]
                            existing_embedding.image_vector = image_vector
                            existing_embedding.updated_at = datetime.now(timezone.utc)
                            print(f"Updated {art_object['object_id']}")
                        else:
                            embedding = Embedding(
                                object_id=art_object["object_id"],
                                image_url=art_object["media_large_url"],
                                image_vector=image_vector,
                                updated_at=datetime.now(timezone.utc),
                            )
                            session.add(embedding)
                            print(f"Added {art_object['object_id']}")

                except Exception as e:
                    print(
                        f"Error with {art_object.get('object_id')}: {str(e)}")

        return True
    except requests.RequestException as e:
        print(f"Error fetching data from {collection_url}: {str(e)}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {collection_url}: {str(e)}")
        return False


def generate_modification_range() -> str:
    now = datetime.now()
    return f"{(now - timedelta(days=1)).strftime('%Y-%m-%d')} TO {now.strftime('%Y-%m-%d')}"


if __name__ == "__main__":
    index_images()
