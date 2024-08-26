from .. import models, schemas, oauth2
from ..database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

# --------QUERY PARAMETERS--------
# LIMIT BY NUMBER OF RESULTS: {{URL}}posts?limit=3 -> Used to implement pagination!
# SKIP POSTS: {{URL}}posts?limit=3&skip=2 
# SEARCH BASED OFF TITLE: {{URL}}posts?limit=3&skip=2&search=ak -> don't enter string in quotation marks
# SPACEBAR IN SEARCH PARAMETER: %20, e.g. search=beautiful%20beaches

# Initialise the router, and how the decorators used to be app.get, change to router.get, or router.post, etc.
router = APIRouter(
    prefix="/posts", # So that we don't have to keep typing in the annoying /posts in the routes
    tags=["Posts"]
)

# ----------------------------------------------------------------------------------------------------

# GET ALL POSTS USING SQLALCHEMY

@router.get("/") # We return posts, which is a list of posts, so import List from typing to coerce to correct data type
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.title.contains(search))\
        .limit(limit).offset(skip).all()
    
    # .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results

# ----------------------------------------------------------------------------------------------------

# GET SINGULAR POST USING SQLALCHEMY

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first() # first() finds first instance of id match

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    
    return post

# ----------------------------------------------------------------------------------------------------

# CREATE NEW POST USING SQLALCHEMY

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(
                                                                          oauth2.get_current_user)):
    # In the code commented out below, we have to list every field as title=post.title, etc...
    # What if we had 50 columns, i.e. 50 fields? It would be very inefficient. Better way to do it is
    # convert to a dictionary using Pydantic and then unpack it. Also, the user_id field comes from the
    # Post(PostBase) schema from schemas.py! We have to provide a user_id for each post. However, it makes
    # sense that the person currently logged in is the same person making the post, so we can set user_id
    # to current_user.id!
    new_post = models.Post(user_id=current_user.id, **post.model_dump())

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    db.add(new_post) # add to database
    db.commit() # commit the changes
    db.refresh(new_post) # retrieve the new post and store back into variable new_post, same as RETURNING *
    return new_post

# ----------------------------------------------------------------------------------------------------

# UPDATE POST USING SQLALCHEMY

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(
                                                                                  oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    first_post = post_query.first()

    if first_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist.')
    
    if first_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this action.')
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return first_post

# ----------------------------------------------------------------------------------------------------

# DELETE POST USING SQLALCHEMY

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(
                                                        oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    
    # If the current user is trying to delete a post made by someone else:
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this action.')
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ----------------------------------------------------------------------------------------------------

# HOW DOES THE AUTHENTICATION PROCESS FOR CREATING A POST WORK?
# - Whenever someone wants to make a post, we want to make sure they are authorized to do so. Imagine 
#   being able to post as someone on Instagram without even logging into their account! 
# - In the create_post function above, it has 3 arguments: 'post' is from schemas.PostCreate, a 'db' Session
#   and 'user_id' that depends on our get_current_user function from our oauth2.py file.
# - The get_current_user function in oauth2.py returns verify_access_token. So the user provides a token
#   (e.g. in Postman, we entered our username and password, and then got the token, which we then put into
#   the headers tab as 'Authentication'), and then we decode that token, and if the ID is a match, then
#   it returns that ID, which is stored in our create_post function as 'user_id'! We can then use that.
# - If the IDs are not a match, the API will return 'not authenticated'.
# - We update the function signature with the user_id that depends on the get_current_user function, so that
#   we can authenticate the user when they try to update or delete posts too.


































# ----------------------------------------------------------------------------------------------------

# GET ALL POSTS USING SQL

# @router.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return posts # Shows all posts saved in memory

# ----------------------------------------------------------------------------------------------------

# CREATE NEW POST USING SQL

# Best practice is to just do /posts, not /createposts
# @router.post("/posts")
# def create_posts(post: schemas.PostCreate, status_code=status.HTTP_201_CREATED):
    
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#                   (post.title, post.content, post.published))
    
#     new_post = cursor.fetchone()

    # conn.commit() # Commits changes to postgres database
    # The reason we use the %s instead of directly passing values is to avoid SQL Injection

    ## PRIMITIVE METHOD WITH ARRAYS AS MEMORY STORAGE
    # post_dict = post.model_dump() # .dict() is deprecated, use .model_dump()
    # post_dict['id'] = randrange(0,10000000)
    # my_posts.append(post_dict)
    
    # return new_post

# ----------------------------------------------------------------------------------------------------

# GET SINGULAR POST USING SQL

# Get specific post, not all posts like above
# @router.get("/posts/{id}")
# def get_post(id: str): # FastAPI will automatically extract the id from the URL and pass it to the function
#     cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) #convert to tuple using comma
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail=f'post with id: {id} was not found') # Raise 404 if invalid ID
    
#     return post

# ----------------------------------------------------------------------------------------------------

# DELETE POST USING SQL

# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):

#     cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()

#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'post with id: {id} does not exist.')
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT) # When you delete smth, you don't want to 
# send anything back except for the 204 status code.

# ----------------------------------------------------------------------------------------------------

# UPDATE POST USING SQL

# @router.put("/posts/{id}")
# def update_post(id: int, post: schemas.PostCreate):

#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""",
#                    (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()

#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'post with id: {id} does not exist.')
    
#     return updated_post

# ----------------------------------------------------------------------------------------------------