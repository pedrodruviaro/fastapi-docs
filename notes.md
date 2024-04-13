# FastAPI - Python

- No vscode, habilitar nas preferências do usuário
- "python.analysis.typeCheckingMode": "basic"
- FastAPI is all based on Pydantic. -> utilizado para validar e converter tipos de dados automaticamente

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

## query params

- boolean params
  -> 1, True, true, on, yes
  -> 0, False, false, off, no
- argumentos obrigatórios devem ser colocados primeiro na lista de argumentos
- lembrar de passar valores default para parâmetros não obrigatórios
- parâmetros opcionais devem receber o default de None

## request body

- request body -> pydantic model
- quando um modelo de um atributo _default_, não é obrigatório

## query parameters and string validations

- podemos declarar informações adicionais e validações para os parãmetros
