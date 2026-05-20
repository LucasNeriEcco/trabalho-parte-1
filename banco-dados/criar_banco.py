"""
Cria o banco restaurante e a tabela prato no MySQL local.
Configure back-end/.env (copie de .env.example) antes de executar.
"""
import argparse
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "back-end"))
load_dotenv(ROOT / "back-end" / ".env")

from config import (  # noqa: E402
    MYSQL_DATABASE,
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USER,
)

CRIAR_BANCO = f"""
CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS prato (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150) NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  descricao TEXT DEFAULT NULL,
  preco DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB
"""


def executar_schema(senha: str | None = None) -> None:
    password = senha if senha is not None else MYSQL_PASSWORD
    if not password or password == "sua_senha_aqui":
        raise SystemExit(
            "Defina MYSQL_PASSWORD em back-end/.env ou use: "
            "python banco-dados/criar_banco.py --senha SUA_SENHA"
        )

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=password,
    )
    try:
        cursor = conn.cursor()
        cursor.execute(CRIAR_BANCO)
        conn.commit()
    finally:
        conn.close()

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=password,
        database=MYSQL_DATABASE,
    )
    try:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        conn.commit()
        print(f"Banco '{MYSQL_DATABASE}' e tabela 'prato' criados com sucesso.")
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cria o banco MySQL do projeto.")
    parser.add_argument("--senha", help="Senha do usuário MySQL (sobrescreve .env)")
    args = parser.parse_args()
    executar_schema(args.senha)
