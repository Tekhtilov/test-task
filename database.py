import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect(
    host="127.0.0.1",
    database="bots_users",
    user="postgres",
    password="Aegis1885"
)

cur = conn.cursor(cursor_factory=DictCursor)
