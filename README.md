# Orders API with JWT

API de pedidos desenvolvida em Python com Flask como parte do curso **Python com Flask da Rocketseat**.

O projeto pratica autenticação com JWT, autorização por usuário, persistência com SQLite, organização baseada em MVC e testes automatizados.

A aplicação permite cadastrar usuários, realizar login, criar pedidos e consultar somente os pedidos pertencentes ao usuário autenticado.

## Contexto

Este projeto foi desenvolvido como desafio prático do curso **Python com Flask da Rocketseat**.

O foco do desafio é aplicar conceitos de autenticação e segurança em uma API, utilizando JWT para identificar usuários e controlar o acesso aos pedidos.

Além da implementação principal, o projeto utiliza hash de senhas, variáveis de ambiente para proteger a chave JWT e testes automatizados para validar os comportamentos mais importantes.

## Funcionalidades

- Cadastro de usuários
- Armazenamento seguro de senhas com hash
- Login de usuários
- Geração de token JWT
- Token contendo ID e username do usuário
- Expiração do token JWT
- Proteção de rotas
- Criação de pedidos
- Associação automática do pedido ao usuário autenticado
- Listagem dos pedidos do usuário autenticado
- Isolamento de pedidos entre usuários
- Persistência de dados com SQLite
- Organização da aplicação com separação baseada em MVC
- Testes automatizados com pytest

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- PyJWT
- Werkzeug
- python-dotenv
- pytest

## Estrutura do projeto

```text
orders-api-jwt/
│
├── app/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── order_controller.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── order.py
│   │   └── user.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── orders.py
│   │   └── users.py
│   │
│   ├── auth.py
│   ├── extensions.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── init_db.py
├── requirements.txt
├── run.py
└── README.md
```

## Como a aplicação funciona

O fluxo principal da API é:

```text
Cadastro do usuário
↓
Login
↓
Geração do JWT
↓
Envio do token nas requisições protegidas
↓
Identificação do usuário
↓
Criação ou consulta dos próprios pedidos
```

O usuário não envia seu próprio `user_id` ao criar um pedido.

A identificação é feita a partir do token JWT recebido durante o login.

Isso evita que um usuário associe manualmente um pedido a outro usuário.

## Banco de dados

A aplicação utiliza SQLite por meio do Flask-SQLAlchemy.

Existem duas tabelas principais.

### users

Campos:

```text
id
username
password
```

O campo `id` identifica o usuário.

O `username` deve ser único.

A senha é armazenada como hash, não em texto puro.

### orders

Campos:

```text
id
description
created_at
user_id
```

Cada pedido possui uma chave estrangeira `user_id`, responsável por relacioná-lo ao usuário proprietário.

## Organização MVC

A aplicação utiliza uma separação simples baseada em MVC.

### Models

Representam as estruturas persistidas no banco:

```text
User
Order
```

### Controllers

Concentram a lógica relacionada aos pedidos, como:

```text
listar pedidos
criar pedidos
```

### Routes

Recebem as requisições HTTP, validam os dados necessários e encaminham a execução para a lógica correspondente.

### View

Como o projeto é uma API, a camada de saída é representada pelas respostas JSON retornadas ao cliente.

A estrutura foi mantida simples e proporcional ao tamanho do projeto.

## Autenticação JWT

Após o login, a API gera um token JWT contendo:

```text
user_id
username
exp
```

O campo `exp` define o momento de expiração do token.

O token precisa ser enviado nas rotas protegidas utilizando o cabeçalho:

```text
Authorization: Bearer TOKEN
```

A aplicação valida o token antes de permitir acesso aos pedidos.

Tokens ausentes, inválidos ou expirados resultam em erro de autenticação.

## Segurança

Algumas medidas aplicadas no projeto:

- senhas não são armazenadas em texto puro;
- a chave JWT não fica escrita diretamente no código;
- a chave JWT é carregada por variável de ambiente;
- o arquivo `.env` não é versionado;
- pedidos são associados automaticamente ao usuário autenticado;
- usuários não conseguem listar pedidos de outros usuários;
- rotas de pedidos exigem autenticação;
- tokens inválidos ou expirados são rejeitados.

## Pré-requisitos

Para executar o projeto é necessário ter:

```text
Python
Git
```

O projeto foi desenvolvido e testado com:

```text
Python 3.14.7
```

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd orders-api-jwt
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell, ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto.

O arquivo `.env.example` possui a estrutura necessária:

```text
JWT_SECRET_KEY=
```

Para gerar uma chave segura, execute:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o valor gerado para o `.env`:

```text
JWT_SECRET_KEY=sua_chave_secreta
```

O arquivo `.env` está configurado no `.gitignore` e não deve ser enviado para o repositório.

## Criando o banco de dados

Execute:

```bash
python init_db.py
```

O script cria as tabelas necessárias.

Quando executado corretamente, a saída deve indicar:

```text
Tables: ['orders', 'users']
```

O banco SQLite é criado localmente dentro da pasta `instance`.

## Executando a aplicação

Com o ambiente virtual ativo:

```bash
python run.py
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

A rota inicial pode ser usada para confirmar que a aplicação está funcionando:

```http
GET /
```

Resposta:

```json
{
  "message": "Orders API is running"
}
```

## Endpoints

### Criar usuário

```http
POST /users
```

Exemplo de requisição:

```json
{
  "username": "waldir",
  "password": "123456"
}
```

Exemplo de resposta:

```json
{
  "id": 1,
  "username": "waldir"
}
```

A senha recebida é convertida em hash antes de ser armazenada.

### Login

```http
POST /login
```

Exemplo:

```json
{
  "username": "waldir",
  "password": "123456"
}
```

Resposta:

```json
{
  "token": "TOKEN_JWT"
}
```

O token deve ser utilizado nas rotas protegidas.

### Criar pedido

```http
POST /orders
```

Requer autenticação.

Cabeçalho:

```text
Authorization: Bearer TOKEN
```

Corpo da requisição:

```json
{
  "description": "Primeiro pedido"
}
```

Exemplo de resposta:

```json
{
  "id": 1,
  "description": "Primeiro pedido",
  "created_at": "2026-10-07T03:49:23.387049"
}
```

O `user_id` não é enviado pelo cliente.

A API utiliza o usuário identificado pelo JWT para definir o proprietário do pedido.

### Listar pedidos

```http
GET /orders
```

Requer autenticação.

Cabeçalho:

```text
Authorization: Bearer TOKEN
```

Exemplo de resposta:

```json
{
  "orders": [
    {
      "id": 1,
      "description": "Primeiro pedido",
      "created_at": "2026-10-07T03:49:23.387049"
    }
  ]
}
```

Somente os pedidos pertencentes ao usuário autenticado são retornados.

## Exemplos com PowerShell

### Cadastro

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/users" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username":"waldir","password":"123456"}'
```

### Login

```powershell
$login = Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username":"waldir","password":"123456"}'

$token = $login.token
```

### Criar pedido

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/orders" `
  -Method POST `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType "application/json" `
  -Body '{"description":"Primeiro pedido"}'
```

### Listar pedidos

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/orders" `
  -Method GET `
  -Headers @{ Authorization = "Bearer $token" }
```

## Testes

Os testes utilizam um banco SQLite em memória para não alterar o banco utilizado durante a execução normal da aplicação.

Execute:

```bash
python -m pytest -v
```

O comando `python -m pytest` é utilizado para garantir que o pytest execute utilizando o mesmo ambiente Python do projeto.

Os testes atuais validam:

- login e geração de JWT;
- presença do `user_id` e `username` no token;
- bloqueio de acesso aos pedidos sem autenticação;
- criação de pedidos por usuário autenticado;
- isolamento dos pedidos entre usuários.

Resultado validado durante o desenvolvimento:

```text
4 passed
```

## Principais conceitos praticados

Durante o desenvolvimento foram aplicados:

- criação de APIs com Flask;
- métodos HTTP;
- autenticação com JWT;
- autorização baseada no usuário autenticado;
- hash de senhas;
- variáveis de ambiente;
- relacionamento entre tabelas;
- SQLite;
- SQLAlchemy;
- separação de responsabilidades;
- MVC aplicado de forma simples;
- tratamento de erros HTTP;
- testes automatizados com pytest;
- banco em memória para testes;
- versionamento incremental com Git.

## Versionamento

O desenvolvimento foi versionado em etapas pequenas.

Entre os checkpoints realizados estão:

```text
configuração inicial
aplicação Flask
configuração do SQLite
models
cadastro de usuários
autenticação JWT
proteção de rotas
criação de pedidos
organização MVC
testes automatizados
```

## Limitações atuais

O projeto implementa somente as funcionalidades necessárias para o desafio atual.

Não foram implementados:

- atualização de pedidos;
- exclusão de pedidos;
- recuperação de senha;
- refresh token;
- interface gráfica;
- deploy em produção.

Esses recursos podem ser adicionados futuramente caso façam parte de uma nova etapa do projeto.

## Status

Desafio prático do curso **Python com Flask da Rocketseat** concluído, com os requisitos principais implementados e testados.

## Autor

**Waldir Évora**
