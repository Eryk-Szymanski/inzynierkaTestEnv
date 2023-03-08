from fastapi import status, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

''' Relatywne importy
'''
from . import crud, models, schemas
from .database import SessionLocal, engine

''' Utworzenie tabel w bazie danych .app/models.py
Base pochodzi z .app/database.py ''' 
models.Base.metadata.create_all(bind=engine)


''' Start aplikacji
'''
app = FastAPI()


''' Ustawienie źródeł CORS
'''
origins = [
    "http://localhost:19006",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


''' Ustwaienie schematu autentyfikacji OAuth2
'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


''' Pobranie zależności do bazy danych
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ścieżki API
#
#
''' Domyślna
'''
@app.get("/")
def read_root():
    return {"Hello": "World"}


''' Autentyfikacja
'''
# Pobranie tokenu do logowania przez OAuth2
@app.post("/token")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Nieprawidłowa nazwa użytkownika lub hasło")
    hashed_password = form_data.password
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Nieprawidłowa nazwa użytkownika lub hasło")

    return {"access_token": user.email, "token_type": "bearer"}


''' Związane z obcenie zalogowanym użytkownikiem
'''
# Pobranie obecnie zalogowanego użytkownika z bazy danych
# Używane przez endpoint /me
async def get_current_user(db: Session = Depends(get_db), username: str = Depends(oauth2_scheme)):
    user = crud.get_user_by_email(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawdiłowe dane logowania",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Sprawdzenie czy obecnie zalogowany użytkownik jest aktywny
# Używane przez endpoint /me
async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Użytkownik nieaktywny")
    return current_user

# Pobranie obecnie zalogowanego użytkownika
@app.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


''' Związane z użytkownikami -> ogólnie
'''
# Utworzenie
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Pobranie wszystkich
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Pobranie po id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
