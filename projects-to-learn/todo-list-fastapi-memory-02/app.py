from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated, Optional
import random

app = FastAPI()


def generate_id() -> str:
    return str(random.randint(1, 100000))


class TodoTagNames(str, Enum):
    house = 'house'
    study = 'study'
    car = 'car'
    uncategorized = 'uncategorized'


class Todo(BaseModel):
    id: Optional[str] = Field(default_factory=generate_id, alias="_id")
    title: str
    tags: list[TodoTagNames] = Field(default_factory=list)
    completed: bool = False


todos: list[Todo] = [Todo(
    title=f"{i}- mock todo", completed=random.choice([True, False])) for i in range(10)]


def get_todo_by_id(id: str) -> Optional[Todo]:
    for todo in todos:
        if todo.id == id:
            return todo
    return None


@app.get('/')
async def root():
    """
    Root endpoint to check available endpoints.
    """
    return {"message": "Check /todos for all todos"}


@app.get('/todos')
async def get_todos():
    """
    Return all todos in memory
    """
    return {"count": len(todos), "data": todos}


@app.get('/todos/{id}')
async def get_todo(id: str):
    todo = get_todo_by_id(id)
    if todo:
        return {"data": todo}

    raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")


@app.patch('/todos/{id}')
async def update_todo(id: str, completed: bool):
    todo = get_todo_by_id(id)
    if todo:
        todo.completed = completed
        return {"data": todo}

    raise HTTPException(status_code=404, detail=f"Todo {id} not found")


@app.post('/todos/create')
async def create_todo(todo: Todo):
    todo.id = generate_id()
    todos.append(todo)

    return {"data": todo}


@app.delete('/todos/{id}')
async def delete_todo(id: str):
    todo = get_todo_by_id(id)
    if todo:
        todos.remove(todo)
        return {"data": todos}

    raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")
