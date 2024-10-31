from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

# Modelo para dados da pessoa
class Pessoa(BaseModel):
    nome: str
    idade: int
    telefone: str
    sexo: str

@app.get("/pessoas")
async def listar_pessoas():
    """Endpoint para listar todas as pessoas."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM pessoas")
            pessoas = cursor.fetchall()
            return {"pessoas": pessoas}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar pessoas: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados")

@app.get("/pessoas/{id}")
async def obter_pessoa(id: int):
    """Endpoint para obter uma pessoa pelo ID."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM pessoas WHERE id = %s", (id,))
            pessoa = cursor.fetchone()
            if pessoa:
                return {"pessoa": pessoa}
            else:
                raise HTTPException(status_code=404, detail="Pessoa não encontrada")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao obter pessoa: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados")

@app.post("/pessoas")
async def criar_pessoa(pessoa: Pessoa):
    """Endpoint para criar uma nova pessoa."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO pessoas (nome, idade, telefone, sexo) VALUES (%s, %s, %s, %s) RETURNING id",
                (pessoa.nome, pessoa.idade, pessoa.telefone, pessoa.sexo)
            )
            connection.commit()
            new_id = cursor.fetchone()[0]
            return {"id": new_id, "mensagem": "Pessoa criada com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar pessoa: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados")

@app.put("/pessoas/{id}")
async def atualizar_pessoa(id: int, pessoa: Pessoa):
    """Endpoint para atualizar uma pessoa pelo ID."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE pessoas SET nome = %s, idade = %s, telefone = %s, sexo = %s WHERE id = %s",
                (pessoa.nome, pessoa.idade, pessoa.telefone, pessoa.sexo, id)
            )
            connection.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Pessoa não encontrada")
            return {"mensagem": "Pessoa atualizada com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar pessoa: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados")

@app.delete("/pessoas/{id}")
async def deletar_pessoa(id: int):
    """Endpoint para deletar uma pessoa pelo ID."""
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM pessoas WHERE id = %s", (id,))
            connection.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Pessoa não encontrada")
            return {"mensagem": "Pessoa deletada com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar pessoa: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados")

