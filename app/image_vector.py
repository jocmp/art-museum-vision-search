import os
import requests

JINA_API_TOKEN = os.environ.get("JINA_API_TOKEN")


def extract_image_vector(value: str) -> list:
    headers = {
        "Authorization": f"Bearer {JINA_API_TOKEN}",
        "Content-Type": "image/jpeg"
    }

    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JINA_API_TOKEN}'
    }
    data = {
        "model": "jina-clip-v2",
        "dimensions": 512,
        "input": [
            {"image": value},
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"API request failed with status code {response.status_code}: {response.text}")

    print(response.text)
    clip_embedding = response.json()['data'][0]['embedding']

    return clip_embedding
