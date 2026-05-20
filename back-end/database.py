from typing import Any

import mysql.connector
from mysql.connector import MySQLConnection

from config import (
    MYSQL_DATABASE,
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USER,
)


def conectar(*, usar_banco: bool = True) -> MySQLConnection:
    params: dict[str, Any] = {
        "host": MYSQL_HOST,
        "port": MYSQL_PORT,
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
    }
    if usar_banco:
        params["database"] = MYSQL_DATABASE
    return mysql.connector.connect(**params)


def linhas_para_dicts(cursor) -> list[dict[str, Any]]:
    colunas = [col[0] for col in cursor.description]
    return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
