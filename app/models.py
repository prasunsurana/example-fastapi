from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False) # nullable means cannot be a null value
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # Has to be
    # same data type as foreign key, i.e. id column from users table. Cascade means if you delete a user,
    # all their posts will be deleted from the posts table. 
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # In social media, we want to see someone's instagram handle, not their user id. So we set up a relationship,
    # when we retrive a post, it will have a property 'owner' that will figure out the relationship. We
    # Update the schema to return a Pydantic class that holds the user id. Look in schemas.py
    user = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True)

