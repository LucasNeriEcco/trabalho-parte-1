# Sabor & Arte — Restaurante (HTML + FastAPI + MySQL)

Projeto educacional com fluxo completo de dados:

**Front-end (HTML/CSS/JS)** -> **API FastAPI** -> **MySQL** -> **API** -> **Front-end**

## Estrutura

- front-end/ — Cadastro e listagem de pratos do cardápio
- back-end/ — API REST em Python (FastAPI)
- banco-dados/ — Script SQL e utilitário para criar o banco

## Pré-requisitos

- Python 3.10+
- MySQL 8.x em execução
- Senha do usuário MySQL (ex.: root)

## 1. Configurar credenciais

Copie o exemplo e informe sua senha do MySQL:

    copy back-end\.env.example back-end\.env

Edite back-end\.env e defina MYSQL_PASSWORD.

## 2. Criar o banco de dados

Opção A — execute banco-dados\setup.bat

Opção B — linha de comando:

    pip install -r back-end/requirements.txt
    python banco-dados/criar_banco.py --senha SUA_SENHA

Isso cria o banco restaurante e a tabela prato.

## 3. Subir a API

    cd back-end
    pip install -r requirements.txt
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

Ou execute back-end\iniciar-servidor.bat.

## 4. Abrir o front-end

Abra front-end\index.html no navegador.

## Endpoints

- GET /pratos — Lista pratos
- POST /pratos — Cadastra prato
- GET /saude — Verifica API e MySQL
