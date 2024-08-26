from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # THe OAuth2 form will come in the format username and password, not email and password!
    # NOTE: When testing if the login works in Postman, go to your User Login request, click Body, but 
    # instead of writing a request dictionary in 'raw', go to 'form-data' and input username/password there
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credentials')
    
    # create token
    # return token

    access_token = oauth2.create_access_token(data={'user_id':user.id})

    return {"access_token": access_token, "token_type": "bearer"}

