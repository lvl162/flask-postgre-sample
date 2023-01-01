import os
import sqlalchemy as db
from dotenv import load_dotenv
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()

load_dotenv()

engine = db.create_engine(
    f"mysql+mysqlconnector://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}?charset=utf8mb4")

conn = engine.connect()
metadata = db.MetaData()

post_table = db.Table('Post', metadata,
                      db.Column('id', db.Integer(), primary_key=True,
                                autoincrement=True),
                      db.Column('content', db.String(255), nullable=False),
                      )

class Post(Base):
    __tablename__ = "Post"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"Post(id={self.id!r}, content={self.content!r})"


metadata.create_all(engine)

session = Session(engine)


def create_post(post):
    new_post = Post(content=post['content'])
    session.add(new_post)
    session.flush()
    session.commit()
    return new_post.id

def get_all():
    posts = [row.as_dict() for row in session.query(Post).all()]
    return posts

def get_post(id_):
    post = session.query(Post).filter(Post.id==id_).first()
    return post.as_dict()

def delete_post(id_):
    return session.execute(delete(Post).where(Post.id == id_)).first()

def update_post(post):
    return session.execute(
        update(Post)
        .where(Post.id == post['id'])
        .values(content=post['content'])
    )
