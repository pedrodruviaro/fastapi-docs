from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from enum import Enum
from random import randint
from typing import Any, Annotated

app = FastAPI()


def generate_id() -> str:
    return str(randint(1, 1000000))


class Category(str, Enum):
    tech = "Tech"
    sports = "Sports"
    news = "News"
    travel = "Travel"
    food = "Food"


class Post(BaseModel):
    id: str = Field(default_factory=generate_id, alias="_id",
                    title="Field ID", description="A unique ID")
    title: str = Field(min_length=5, max_length=140)
    content: str = Field(min_length=2)
    category: Category
    tags: set[str] = set()
    is_private: bool = Field(default=False)
    my_secret: bool = Field(default=False)


posts: list[Post] = [
    Post(title=f"My custom post {i}", content=f"Some content for post {i}", category=Category.food) for i in range(5)
]


def search_post_by_id(id: str) -> Post | None:
    for post in posts:
        if post.id == id:
            return post
    return None


@app.get("/")
async def root():
    return {"message": "All good - API is running"}


@app.get("/posts", response_model=list[Post])
async def get_posts(q: Annotated[str | None, Query(min_length=1, max_length=50)] = None) -> Any:
    posts_to_return: list[Post] = []
    if q:
        for post in posts:
            if q.lower() in post.title.lower():
                posts_to_return.append(post)
        return posts_to_return

    posts_to_return = posts
    return posts_to_return


@app.get("/posts/{id}", response_model=Post)
async def get_post_by_id(id: Annotated[str, Path(min_length=3)]) -> Any:
    post = search_post_by_id(id)
    if post:
        return post
    raise HTTPException(status_code=404, detail=f"Post {id} not found")


@app.post("/posts", response_model=Post)
async def create_post(post: Post) -> Any:
    posts.append(post)
    return post


@app.put("/posts/{id}", response_model=Post)
async def update_post_by_id(id: Annotated[str, Path(min_length=2, title="Post ID")], updatedPost: Post) -> Any:
    for index, post in enumerate(posts):
        if post.id == id:
            updatedPost.id = post.id
            posts[index] = updatedPost
            return updatedPost
    raise HTTPException(status_code=404, detail=f"Post {id} not found")


@app.delete("/posts/{id}", response_model=Post)
async def delete_post_by_id(id: Annotated[str, Path(min_length=2, title="Post ID")]) -> Any:
    for index, post in enumerate(posts):
        if post.id == id:
            del posts[index]
            return post
    raise HTTPException(status_code=404, detail=f"Post {id} not found")
