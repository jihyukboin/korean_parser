import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB"),
)

cursor = conn.cursor()

cursor.execute("select Now();")

print(cursor.fetchone())

