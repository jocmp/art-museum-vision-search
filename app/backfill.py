import os
import requests
import json
from PIL import Image
from io import BytesIO

from app.db import db_session
from app.image_vector import extract_image_vector, init_models
from app.models.embedding import Embedding


def backfill():
    init_models()

    base_collection_url = os.environ.get("ART_MUSEUM_COLLECTION_URL")
    limit = 50
    start = 0

    while True:
        collection_url = f"{base_collection_url}/objectSearch?q=*&limit={limit}&start={start}"

        try:
            response = requests.get(collection_url)
            response.raise_for_status()

            data = response.json()

            temp_files = []

            filtered_data = {k: v for k, v in data.items() if k.isdigit()}

            # Stop if no more data
            if not filtered_data:
                break

            print(
                f"Processing {len(filtered_data)} items starting from {start}")

            for _, art_object in filtered_data.items():
                if "media_large_url" in art_object:
                    try:
                        img_response = requests.get(
                            art_object["media_large_url"])
                        img_response.raise_for_status()

                        image = Image.open(BytesIO(img_response.content))
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

            # Increment start for next batch
            start += limit

        except requests.RequestException as e:
            print(f"Error fetching data from {collection_url}: {str(e)}")
            break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {collection_url}: {str(e)}")
            break

    return temp_files


if __name__ == "__main__":
    backfill()
