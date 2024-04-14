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
