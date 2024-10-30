from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import OperationalError

app = FastAPI()

# Configurações do banco de dados
DB_HOST = "autorack.proxy.rlwy.net"
DB_PORT = 51627
DB_NAME = "railway"
DB_USER = "postgres"
DB_PASSWORD = "KOCWFRTKpnfOkVUGffqTBKpsyhMNzhpu"

def connect_to_database():
    """Função para conectar ao banco de dados PostgreSQL."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.get("/test-connection")
async def test_connection():
    """Endpoint para testar a conexão com o banco de dados."""
    connection = connect_to_database()
    if connection is not None:
        connection.close()
        return {"status": "Conexão bem-sucedida com o banco de dados!"}
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados")

