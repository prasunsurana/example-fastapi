from passlib.context import CryptContext

# Tells passlib to use bcrypt as the default hashing algorithm to securely store user passwords in the database.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto") 

# Hashes the password
def hash(password: str):
    return pwd_context.hash(password)

# Takes in the raw password, hashes, then compares to the database hashed password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
