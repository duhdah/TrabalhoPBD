import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="PET",
        user="postgres",
        password="123123"
    )