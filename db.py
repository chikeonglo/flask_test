import psycopg2

def connect():
    c = psycopg2.connect('dbname=flask-sql-snack', user='postgres', password=123456)
    return c

def get_all_snacks():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM snacks")
    snacks = cur.fetchall()
    cur.close()
    conn.close()
    return snacks

def add_snack(name, kind):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO snacks (name, kind) VALUES (%s, %s)", (name, kind))
    conn.commit()
    cur.close()
    conn.close()

def edit_snack(name, kind, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE snacks SET name = %s WHERE id = %s;", (name, id))
    cur.execute("UPDATE snacks SET kind = %s WHERE id = %s;", (kind, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_snack(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM snacks WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
