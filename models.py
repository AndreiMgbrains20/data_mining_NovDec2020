from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table
)

Base = declarative_base()

"""
many to one _> one to many
many to many
"""

tag_post = Table(
    'tag_post',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)
#
# comment_post = Table(
#     'comment_post',
#     Base.metadata,
#     Column('post_id', Integer, ForeignKey('post.id')),
#     Column('comment_id', Integer, ForeignKey('comment.id'))
# )


# todo POST table
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False, unique=False)
    img_url = Column(String, nullable=True, unique=False)
    date_time = Column(DateTime, nullable=False, unique=False)
    write_id = Column(Integer, ForeignKey('writer.id'))
    writer = relationship("Writer")
    tags = relationship('Tag', secondary=tag_post)
    comments = relationship('Comment')

# todo TAG table
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    url = Column(String, unique=False, nullable=False)
    name = Column(String, unique=False, nullable=False)
    posts = relationship('Post', secondary=tag_post)

# todo Writer table
class Writer(Base):
    __tablename__ = 'writer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=False)
    url = Column(String, nullable=False, unique=True)
    posts = relationship("Post")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    # url = Column(String, unique=False, nullable=False)
    name = Column(String, unique=False, nullable=False)
    text = Column(String, unique=False, nullable=False)
    posts = relationship('Post')