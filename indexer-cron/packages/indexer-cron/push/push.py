import os


def main():
    vision_search_url = os.getenv('VISION_SEARCH_URL')
    indexer_secret = os.getenv('INDEXER_SECRET')

    if not vision_search_url or not indexer_secret:
        return {"error": "missing secrets"}

    return {"status": "OK"}
