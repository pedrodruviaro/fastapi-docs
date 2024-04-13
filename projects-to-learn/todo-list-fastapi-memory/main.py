import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Todo(BaseModel):
    id: str | None = None
    content: str


todos: list[Todo] = []


@app.get('/todos')
async def get_todos():
    return todos


@app.get('/todos/{id}')
async def get_todo(id: str):
    for todo in todos:
        if todo.id == id:
            return {"todo": todo}
    return HTTPException(status_code=404, detail=f"Todo {id} not found")


@app.post('/todos/new')
async def create_todo(todo: Todo):
    id = str(random.randint(1, 1000000))
    todo_dict = todo.model_dump()
    todo_dict.update({"id": id})

    todos.append(Todo(**todo_dict))

    return {"msg": "Todo created", "todos": todos}


@app.delete("/todos/{id}")
async def detele_todo(id: str):

    for idx, todo in enumerate(todos):  # enumerate retorna chave-valor
        if todo.id == id:
            del todos[idx]
            return {"todos": todos}

    raise HTTPException(status_code=404, detail="Todo not found")
