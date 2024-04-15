# FastAPI - Python

> Seguindo a documentação oficial e testando coisas
>
> https://fastapi.tiangolo.com/learn/

- No vscode, habilitar nas preferências do usuário
- **"python.analysis.typeCheckingMode": "basic"**
- FastAPI é toda baseada no Pydantic. -> utilizado para validar e converter tipos de dados automaticamente

## Iniciando um project com fast api

- criando o venv

  - $ pip install virtualenv
  - $ python3 -m venv env
  - $ source env/bin/activate
  - $ pip install "uvicorn[standard]"

  - para sair do venv -> $ source deactivate

- **nota sobre o github**

  - não subimos a pasta env nem **pycache** ao gh. Para isso, criamos um arquivo requirements.txt que leva os dados necessários para a instalação dos pacotes.
  - para gerar o arquivo
    - $ pip freeze > requirements.txt
  - quando o repositório for baixado, basta criar um novo ambiente virtual e installar os pacotes (dentro da venv)
    - $ python3 -m venv env
    - $ pip install -r requirements.txt

- para rodar o projeto

  - $ uvicorn main:app --reload

    - main -> arquivo main.py
    - app -> nome da instância do fastapi (app = FastApi())

  - a aplicação roda por padrão na porta 8000 (http://127.0.0.1:8000)
  - a documentação gerada pela OpenAPI fica na rota /docs -> http://127.0.0.1:8000/docs

- @app.get('/') -> path operation decorator
  - a função declarada abaixo será a executada quando a rota for acionada

## Path Parameters

- convertidos automaticamente para a mesma tipagem definida
- retornam erro se não passados na tipagem definida
- podemos definir Enums que retornam erro caso não sejam fornecidos
- toda a documentação de parâmetros fica disponível na mesma documentação (/docs ou /redocs)

```py
@app.get('/foo/{bar}')
def foo_handler(bar: str):
    return {"param": bar}
```

## Query Parameters

- boolean params
  -> 1, True, true, on, yes
  -> 0, False, false, off, no
- argumentos obrigatórios devem ser colocados primeiro na lista de argumentos
- lembrar de passar valores default para parâmetros não obrigatórios
- parâmetros opcionais devem receber o default de None

```py
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
```

## Request Body

- request body -> pydantic model
- quando um modelo de um atributo _default_, não é obrigatório

```py
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

## Query parameters and string validations

- podemos declarar informações adicionais e validações para os parãmetros

```py
@app.get("/items")
async def get_items2(q: Annotated[str | None, Query(
        title="Query string",
        description="My custom validation",
        min_length=2,
        max_length=50
)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return []
    return results
```

## Path Parameters and Validations

```py
@app.get('/books/{id}')
async def get_book_by_id(id: Annotated[int, Path(title="ID is a required param", gt=2, le=100)]):
    return {"id": id}
```

## Body - Fields

- utilizamos o _Field_ do pydantic para aumentar o nível da validação dos modelos

```py
class Item(BaseModel):
    title: str = Field(min_length=2, max_length=100, title="Title field",
                       description="String field to define a title")
    is_paid: bool | None = Field(default=None, title="")
    price: float | None = Field(default=None, title="", gt=0)
    tax: float | None = None
    id: int = Field(default_factory=generate_id, alias="_id")

```

- nesse exemplo, _generate_id_ é uma função que retorna um inteiro

## Body - Nested models

- python > 3.9 utilizamos List do módulo typing para definir lista nos modelos

```py
class Book(BaseModel):
    tags: List[str] = []
```

- nesse exemplo, tags não deveriam se repetir. Podemos usar então o tipo _set_. Assim, se houver dados repetidos na requisição, os valores serão tratados e removidos.

```py
class Book(BaseModel):
  tags: set[str] = set()
```

- submodelos como tipo também são válidos
  - útil para adicionar validação, documentação, type hints e data conversion.

```py
class Image(BaseModel):
  url: str
  alt: str

class Post(BaseModel):
  title: str
  tags: set[str] = set()
  image: Image | None = None

```

- temos outros tipos válidos no pydantic -> https://docs.pydantic.dev/latest/concepts/types/
- um deles é o _HttpUrl_, que permite validar strings no formato http.

```py
class Link(BaseModel):
  href: HttpUrl
  label: str
```

## Declare Request Example Data

- podemos declarar esquemas JSON para usar como exemplo de requisição
- os exemplos aparecem na documentação para auxiliar

```py
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "foo",
                    "description": "bar",
                    "price": 4.5,
                    "tax": 0.25
                }
            ]
        }
    }
```

## Extra Data Types

- UUID
- datetime.datetime
  - 2008-09-15T15:53:00+05:00
- datetime.date
  - 2008-09-15

## Header Parameters

- usamos os Header() como tipo
- \_ é convertido em _-_ e _snake_case_ é convertido para _CammelCase_ pelo fastAPI. Ou seja, \_user*agent* vira **User-Agent**

```py
@app.get('/header')
async def header_handler(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

- ao invés de somente _str_, podemos receber também _list[str]_ caso seja necessário

## Request Model - Return Type

- útil quando queremos retornar apenas parte dos dados, mas não todos. Ex: retornar apenas alguns campos do modelo
- podemos definir o retorno do path operation
- com isso, o retorno é validado pela FastAPI e adicionado um JSON Schema na documentação da OpenAPI
- **limita e filtra a saída de dados da aplicação**

```py
# pode retornar a lista
@app.post("/store/item/new")
async def create_store_item(item: StoreItem) -> list[StoreItem]:
    items.append(item)
    return items

# ou um item específico
@app.post("/store/item/new")
async def create_store_item(item: StoreItem) -> StoreItem:
    return item

```

### response_model param

- em alguns casos precisamos retornar um tipo diferente de dado, não todo o modelo. Definimos isso no parâmetro _response_model_ no decorator.

```py
@app.get("/items", response_model=Item) # pode ser list[Item]
async def get_user(item: Item) -> Any:
  return item
```

- um bom exemplo é aceitar um usuário completo e retornar alguns dados (sem a senha, por ex)

```py
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

```

- nesse caso, estamos retornando user (que deveria conter o campo de senha) mas o FastAPI filtra os dados e retorna apenas o necessário.

- obs: **EmailStr** é um pacote do pydantic -> https://arc.net/l/quote/fveojhev

  - instalar com $ pip install email-validator ou $ pip install pydantic[email]

- o uso do _response_model_ se dá pois os editores podem reclamar da falta ou excesso de parâmetros no retorno. Colocando no decorator, o filtro dos campos é feito e tudo funciona. A documentação é atualizada da mesma forma.

### Return Type and Data Filtering

- podemos utilizar herança para definir o tipo de retorno
- dessa forma, os editors não retornarão erro nem problemas de tipagem
  - type notations, data filter e tooling support
- automaticamente coloca nos docs o tipo de entrada e saída

```py
class BaseUser(BaseModel):
    email: str
    username: str


class UserIn(BaseUser):
    password: str = Field(title="Senha", min_length=6, max_length=20)


@app.post('/users')
async def create_user(user: UserIn) -> BaseUser:
    return user
```

- utilizando _response_model_exclude_unset=True_ como parâmetro no decorator não retornaremos os campos com valor **default** que não estiverem no corpo da requisição

```py
@app.post("/endpoint", response_model_exclude_unset=True)
```

## Extra Models

- em alguns casos podemos ter mais de uma relação de modelo. Por exemplo: um modelo de usuário recebido, um de retornado e um para salvar no banco de dados
- um exemplo dessa funcionalidade

```py

class UserIn(BaseModel):
    email: str
    password: str
    username: str


class UserOut(BaseModel):
    email: str
    username: str


class UserDb(BaseModel):
    email: str
    username: str
    hashed_password: str


def generate_hashed_password(value: str) -> str:
    return f"mYsEcReT-{value}"


def save_user(user: UserIn):
    hashed_password = generate_hashed_password(user.password)
    user_dict = user.model_dump()

    user_in_db = UserDb(**user_dict, hashed_password=hashed_password)
    print("User saved! ..not really")
    print(user_in_db)
    return user_in_db


@app.post('/users', response_model=UserOut)
async def create_user(user: UserIn):
    saved_user = save_user(user)

    return saved_user
```

- _response_model_ também pode recber um Union

```py
response_model=Union[CarModel, PlaneModel] # CarModel | PlaneModal não é uma sintaxe válida aqui
```

- _response_model_ também pode receber uma lista de modelos -> **list[CarModel]**

## Response Status Code

- podemos declarar o status da responsa no decorator

```py
@app.post("/users", status_code=201)
async def create_user()
  ...
```

- ao invés de decorar os status, podemos utilizar o helper _status_ importado de _fastapi_
  - o valor é exatamente o mesmo. Serve apenas como facilitador na hora de escrever o código

```py
from fastapi import status

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user()
  ...

```

## Handling Errors

- para tratar erros nas respostas utilizamos a clase _HTTPException_ do _fastapi_.
- não retornamos ela, usamos um _raise_

```py
from fastapi import HTTPException

async def get_user()
  raise HTTPException(status_code=404, detail="Item not found")
```

## Path Operation Configuration

- podemos passar outros parâmetros ao decorator (_path operation decorator_), além dos já vistos anteriormente

### **tags**

- útil para criar abas na documentação

```py
@app.post("/items/", tags=["items"]) # pode ser um Enum (útil em grandes aplicações) -> tags=[Tags.items]
```

### summary and description

- podemos prover algumas informações extras para fins de documentação

```py
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
    response_description="The created item"
)
```

- no caso de descrições mais longas, podemos usar o dosctring e escrever direto na função do path operation entre aspas triplas
  - nesse caso, markdown é suportado

### deprecated

- caso precise colocar uma rota como _deprecated_, basta passar o parâmetro _deprecated=True_

## Body - Updates

- utilizando o PUT, trocaremos o conteúdo inteiro do dado pelo recebido na requisição
- podemos utilizar o _jsonable_encoder_ para passar o dado recebido para o formado JSON

```py
from fastapi.encoders import jsonable_encoder
update_item_encoded = jsonable_encoder(item)
```

- obs: operações de PUT trocam todos os dados, ou seja, valores default podem ser reescritos se não forem passados na requisição

## CORS - (Cross-Origin Resource Sharing)

```py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
