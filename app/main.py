from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.responses import JSONResponse

from app.search.related_images import search_related_images


app = FastAPI()


@app.post("/search")
async def search(image: UploadFile):
    try:
        result = await search_related_images(image)

        return JSONResponse(content={"results": result})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing image: {str(e)}"}
        )
