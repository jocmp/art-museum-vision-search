import os
import requests
import json
from PIL import Image
from io import BytesIO

from app.db import db_session
from app.image_vector import extract_image_vector
from app.models.embedding import Embedding


def index_images():
    base_collection_url = os.environ.get("ART_MUSEUM_COLLECTION_URL")
    collection_url = f"{base_collection_url}/objectSearch?q=AI_test_set"

    try:
        response = requests.get(collection_url)
        response.raise_for_status()

        data = response.json()

        temp_files = []

        filtered_data = {k: v for k, v in data.items() if k.isdigit()}

        for _, art_object in filtered_data.items():
            if "media_large_url" in art_object:
                try:
                    img_response = requests.get(art_object["media_large_url"])
                    img_response.raise_for_status()

                    image = Image.open(BytesIO(img_response.content))
                    print(
                        f"Loaded image: {image.format}, size: {image.size}, mode: {image.mode}")
                    image_vector = extract_image_vector(image)

                    with db_session() as session:
                        embedding = Embedding(
                            object_id=art_object["object_id"],
                            image_url=art_object["media_large_url"],
                            image_vector=image_vector
                        )

                        session.add(embedding)

                except Exception as e:
                    print(
                        f"Error with {art_object.get('object_id')}: {str(e)}")

        return temp_files

    except requests.RequestException as e:
        print(f"Error fetching data from {collection_url}: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {collection_url}: {str(e)}")
        return []
