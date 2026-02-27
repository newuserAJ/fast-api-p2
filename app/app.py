from fastapi import FastAPI,HTTPException
from app.schema import PostCreate,PostResponse
from app.db import create_db,get_async_session,Post
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

async def lifespan(app:FastAPI):
    await create_db()
    yield

app=FastAPI(lifespan=lifespan)
blog_posts = {
    1: {"title": "Getting Started", "content": "Every expert was once a beginner. Start small, stay consistent."},
    2: {"title": "Dev Note", "content": "Write code as if someone else will maintain it tomorrow."},
    3: {"title": "AI Insight", "content": "Data quality matters more than model complexity."},
    4: {"title": "Productivity", "content": "Deep work beats multitasking every single time."},
    5: {"title": "Fun Fact", "content": "Python was named after Monty Python, not the snake."},
    6: {"title": "Backend Tip", "content": "Validate inputs at the API boundary to prevent bugs downstream."},
    7: {"title": "Security Reminder", "content": "Never trust user input—always sanitize and validate."},
    8: {"title": "Database Thought", "content": "Indexes speed up reads but can slow down writes."},
    9: {"title": "Quote", "content": "First, solve the problem. Then, write the code."},
    10: {"title": "Cloud Update", "content": "Containerization simplifies deployment across environments."},
    11: {"title": "Weekend Build", "content": "Planning to refactor my old FastAPI project for better structure."},
    12: {"title": "Debug Log", "content": "If it works in production but not locally, check environment variables."},
    13: {"title": "Learning Note", "content": "Understanding fundamentals makes advanced concepts easier."},
    14: {"title": "Architecture", "content": "Separate business logic from routing for maintainable APIs."},
    15: {"title": "Mini Announcement", "content": "New backend feature rolling out with improved performance."}
}
@app.get("/")
def getter(limit:int | None =None):
    if limit:
        return list(blog_posts.items())[:limit]
    return blog_posts

@app.get("/posts/{id}")
def finder(id:int):
    data=getter()
    if id not in data:
        raise HTTPException(status_code=404,detail=f"product id {id} not found")
    return data.get(id)

@app.post("/posts")
def create_post(post:PostCreate)->PostCreate:
     new_post={"title":post.title,"content":post.content}
     new_id=max(blog_posts.keys())+1
     blog_posts[new_id]=new_post
     return new_post


@app.delete("/products/{id")
def delete_post(id:int):
    post_id=getter().keys()
    if id not in post_id:
        raise HTTPException(status_code=404,detail=f"Product with id {id} not found")
    deleted=blog_posts.pop(id)
