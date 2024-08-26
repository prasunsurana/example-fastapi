from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, vote

# NOTES:
# - the command to run the API commands is 'uvicorn [file name]:[app name] --reload
# - So in this case, it is uvicorn main:app --reload. reload is a flag to automatically restart the API
#   when changes are made to the code.
# - Look down to the get_post function (i.e. get singular post). Lets say we wanted to get the latest 
#   post, so we create another function called get_latest, and the path in the decorator is /posts/latest.
#   If this function comes after the get_post function, FastAPI will read through our script in order
#   and treat the '/latest' in the path as an ID! So ORDER MATTERS, we have to put the get_latest 
#   function FIRST, and the get_post function SECOND.
# - To see API documentation, you don't need to write anything. FastAPI has inbuilt auto-documentation,
#   so just go to 127.0.0.1/8000[or whatever port]/docs[or redoc for different format]
# - SQLAlchemy is an Object Relational Mapper (ORM).
# - SQLAlchemy doesn't really modify tables once they are created. To do this, you need to use 
#   database migration tools like Alembic.
#   So if you modify a data field in the table, for example, SQLAlchemy won't update it. You'll have to
#   delete the table then remake it again for those changes to take place.
# - IMPORTANT NOTE: There are two types of 'schemas' here. The class Post that inherits from Pydantic
#   BaseModel defines the structure of the REQUEST we make to the database. The Post that we defined using
#   SQLAlchemy in models.py defines the schema for the DATABASE COLUMNS.

# Takes all the classes that inherit from Base and connects them to the database
# models.Base.metadata.create_all(bind=engine) 

# NOTE: Above, we commented out this line of code that told SQLAlchemy to create all the tables when it
# first started up. But since we have Alembic now, we don't need it anymore. We can un-comment it and it
# won't break anything, but no real use for it. If we didn't use alembic, we would still need this^.

app = FastAPI()

origins = ["*"]

# allow methods also allows us to control which type of requests are permitted, such as POST, PUT, etc
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------------------------------------------------------------------------------------------------

# Use Routers to keep main.py file uncluttered. Separate the posts and users routes/functions into
# other files for organisation. Check those other files for router creation!
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# DONT NEED THIS
@app.get("/")
async def root(): # async is optional
    return {"message": "welcome to my api, people!!"}


