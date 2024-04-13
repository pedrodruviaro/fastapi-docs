from fastapi import FastAPI, Query
from pydantic import BaseModel
from enum import Enum
from typing import Annotated

app = FastAPI()


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


class UsersRole(int, Enum):
    admin = 1
    user = 2


@app.get('/')
async def root():
    return {'message': "Hello fastapi"}


@app.get('/foo/{bar}')
def foo_handler(bar: str):
    return {"param": bar}


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return 'alexnet!!!'
    if model_name.value == 'lenet':
        return 'lenet!!'

    return {"model_name": model_name, 'message': "Have some residuals"}


@app.get('/user/roles/{user_role}')
async def get_user_role(user_role: UsersRole):
    if user_role is UsersRole.admin:
        return 'is admin'
    if user_role.name == 'user':
        return 'us user'


@app.get('/items/{item_id}')
async def get_items(item_id: str, needy: str, skip: int = 0, limit: int = 10, q: str | None = None, kill: bool = True):
    if not kill:
        return {"msg": "not today", 'needy': needy}

    if q:
        return {
            "q": q,
            "item_id": item_id
        }
    else:
        return {
            "item_id": item_id
        }


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.model_dump()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": round(price_with_tax, 2)})

        return item_dict

    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


@app.get("/items")
async def get_items(q: Annotated[str | None, Query(
        title="Query string",
        description="My custom validation",
        min_length=2,
        max_length=50
)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
