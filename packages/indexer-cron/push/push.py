import os
import urllib.request
import urllib.error
import json


def main():
    vision_search_url = os.getenv('VISION_SEARCH_URL')
    indexer_secret = os.getenv('INDEXER_SECRET')

    if not vision_search_url or not indexer_secret:
        return {"error": "missing secrets"}

    try:
        req = urllib.request.Request(
            f'{vision_search_url}/index-images',
            method='POST',
            headers={
                'X-Indexer-Secret': indexer_secret,
                'Content-Type': 'application/json'
            }
        )

        with urllib.request.urlopen(req) as response:
            if response.status >= 400:
                raise urllib.error.HTTPError(
                    response.url, response.status, response.reason, response.headers, response)

    except urllib.error.URLError as e:
        return {"error": f"Request failed: {str(e)}"}
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP error {e.code}: {e.reason}"}

    return {"status": "OK"}
