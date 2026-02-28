from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from app.schema import PostResponse
from app.db import create_db, get_async_session, Post
from app.images import image_kit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import tempfile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello():
    return {"message": "Hello User"}


# Upload + Save to DB
@app.post("/upload", response_model=PostResponse)
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    temp_file_path = None

    try:
        # Save temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # Upload to ImageKit
        with open(temp_file_path, "rb") as f:
            upload_result = image_kit.upload(
                file=f,
                file_name=file.filename,
                options=UploadFileRequestOptions(
                    use_unique_file_name=True,
                    tags=["backend-upload"]
                ),
            )

        if not upload_result.url:
            raise HTTPException(
                status_code=400,
                detail="File upload failed"
            )

        # Save DB entry
        post = Post(
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type == "video/mp4" else "image",
            file_name=upload_result.file_name,
        )

        session.add(post)
        await session.commit()
        await session.refresh(post)

        return post

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


# Feed endpoint
@app.get("/feed", response_model=list[PostResponse])
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Post).order_by(Post.created_at.desc())
    )
    posts = result.scalars().all()
    return posts
