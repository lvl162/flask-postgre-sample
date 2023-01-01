import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor
import models as repo

load_dotenv()

app = Flask(__name__)

@app.get("/")
def hello_world():
    return '<h1>Hello, World</h1>'


@app.put("/api/posts/<id>")
def update_post(id):
    data = request.get_json()
    data['id']=id
    repo.update_post(data)
    return {"id": id, "message": f"Post {id} updated."}, 201


@app.post("/api/posts")
def create_new_post():
    data = request.get_json()
    new_id = repo.create_post(data)   
    return {'id': new_id, "message": "OK"}, 201


@app.get("/api/posts/<id>")
def get_post_by_id(id):
    post = repo.get_post(id)
    return {"id": id, 'content': post}, 200


@app.get("/api/posts")
def get_posts():
    posts = repo.get_all()
    return jsonify(posts), 200
