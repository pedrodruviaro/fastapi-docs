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

## path params

- convertidos automaticamente para a mesma tipagem definida
- retornam erro se não passados na tipagem definida
- podemos definir Enums que retornam erro caso não sejam fornecidos
- toda a documentação de parâmetros fica disponível na mesma documentação (/docs ou /redocs)

```py
@app.get('/foo/{bar}')
def foo_handler(bar: str):
    return {"param": bar}
```

## query params

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

## request body

- request body -> pydantic model
- quando um modelo de um atributo _default_, não é obrigatório

```py
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

## query parameters and string validations

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

## path parameters and validations

```py
@app.get('/books/{id}')
async def get_book_by_id(id: Annotated[int, Path(title="ID is a required param", gt=2, le=100)]):
    return {"id": id}
```
