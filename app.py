import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from psycopg2.extras import RealDictCursor

load_dotenv()

app = Flask(__name__)

connection = psycopg2.connect(
    f"""dbname={os.environ.get('DB_NAME')} 
        user={os.environ.get('DB_USER')}
        host={os.environ.get('DB_HOST')}
        password={os.environ.get('DB_PASSWORD')}
        port={int(os.environ.get('DB_PORT'))}""")


def init_data(conn):
    print('--- Insert sample data ---')
    cur = conn.cursor()
    cur.execute("""
                SELECT EXISTS (
                SELECT FROM 
                    pg_tables
                WHERE 
                    schemaname = 'public' AND 
                    tablename  = 'posts'
                );
                """)
    is_exist_posts = cur.fetchone()[0]
    if not is_exist_posts:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS public.posts (
                    post_id serial primary key,
                    content VARCHAR(200)
                    );
                    insert into public.posts(content) values('Sample content 1');
                    insert into public.posts(content) values('Sample content 2');
                    insert into public.posts(content) values('Sample content 3');
                    insert into public.posts(content) values('Sample content 4');
                    insert into public.posts(content) values('Sample content 5');
                    """
                    )
        conn.commit()


@app.get("/")
def hello_world():
    return '<h1>Hello, World</h1>'


@app.put("/api/posts/<id>")
def update_post(id):
    data = request.get_json()
    content = data["content"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "update table posts set content=(%s) where post_id=(%d)", (content, id))
            post_id = cursor.fetchone()[0]
    return {"id": post_id, "message": f"Post {content} updated."}, 201


@app.post("/api/posts")
def create_post():
    data = request.get_json()
    content = data["content"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "insert into posts(content) values(%s) RETURNING post_id", (content,))
            post_id = cursor.fetchone()[0]
    return {"id": post_id, "message": f"Post {content} created."}, 201


@app.get("/api/posts/<id>")
def get_post(id):
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT post_id, content FROM posts WHERE post_id = (%s)", (id,))
            post = cursor.fetchone()
    return {"id": id, "content": post}, 200


@app.get("/api/posts")
def get_posts():
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT post_id, content FROM posts")
            posts = cursor.fetchall()
    return {"content": posts}, 200


init_data(connection)
