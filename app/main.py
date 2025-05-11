import os
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from alembic.config import Config
from alembic import command

# from app.image_vector import init_models

# from fastapi import UploadFile
# from fastapi.responses import JSONResponse

# from app.search.related_images import search_related_images

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = Config()
    config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))
    config.set_main_option('script_location', 'app/alembic')
    command.upgrade(config, 'head')
    # init_models()
    yield

app = FastAPI(lifespan=lifespan)


# @app.post("/search")
# async def search(image: UploadFile):
#     try:
#         result = await search_related_images(image)

#         return JSONResponse(content={"results": result})
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"Error processing image: {str(e)}"}
#         )


@app.get("/")
async def health():
    return {"status": "OK"}
