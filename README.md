# CandyShop

## Requisitos Pré-Instalação

- Python 3.11+
- Poetry
- Git (opcional, mas recomendado)

## Configuração do Ambiente

### 1. Clonar esse o Repositório ou fazer o download do .rar

### 2. Instalar Poetry

```bash
pip install poetry
```

### 3. Instalar Dependências

```bash
poetry install
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
```

(necessario gerar uma 'senha de aplicativo' na sua conta gmail para acessos externos)

### 5. Configurar Banco de Dados

```bash
poetry run python candyshop/manage.py makemigrations
poetry run python candyshop/manage.py migrate
```

### 6. Criar Usuário Administrador (Opcional) para acessar o painel administrador http://127.0.0.1:8000/admin/

- use o usuario padrao:
  usuario: admin
  senha: admin

ou crie o seu proprio com o comando:

```bash
poetry run python candyshop/manage.py createsuperuser
```

### 7. Rodar o Projeto

```bash
poetry run poe start
```

O projeto estará disponível em `http://127.0.0.1:8000/`

## Comandos Úteis do Poetry

- Ativar ambiente virtual: `poetry shell`
- Instalar dependência: `poetry add nome-pacote`
- Instalar dependência de desenvolvimento: `poetry add --group dev nome-pacote`

## Estrutura do Projeto

- `candyshop/`: Pasta principal do projeto Django
- `templates/`: Templates HTML
- `media/`: Arquivos de mídia
- `static/`: Arquivos estáticos (CSS, JS)

## Dependências Principais

- Django 4.2.4
- Python 3.11
- Pillow
- Requests
- QRCode
