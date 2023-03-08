from fastapi import status, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
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
# Pobranie schematu sklepu
@app.get("/", response_class=FileResponse)
async def read_root():
    return "./app/images/storemap.jpg"


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
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Pobranie wszystkich
@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Pobranie po id
@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


''' Związane ze sklepami
'''
# Utworzenie
@app.post("/stores/", response_model=schemas.Store)
async def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    db_store = crud.get_store_by_address(db, address=store.address)
    if db_store:
        raise HTTPException(status_code=400, detail="Sklep z tym samym adresem już istnieje")
    return crud.create_store(db=db, store=store)

# Pobranie wszystkich
@app.get("/stores/", response_model=list[schemas.Store])
async def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    stores = crud.get_stores(db, skip=skip, limit=limit)
    return stores

# Pobranie po id
@app.get("/stores/{store_id}", response_model=schemas.Store)
async def read_store(store_id: int, db: Session = Depends(get_db)):
    db_store = crud.get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_store


''' Związane ze schematami
'''
# Utworzenie
@app.post("/store_schemas/", response_model=schemas.StoreSchema)
async def create_store_schema(store_schema: schemas.StoreSchemaCreate, db: Session = Depends(get_db)):
    db_store_schema = crud.get_store_schema_by_store_id(db, store_id=store_schema.store_id)
    if db_store_schema:
        raise HTTPException(status_code=400, detail="Schemat sklepu związany z tym sklepem już istnieje")
    return crud.create_store_schema(db=db, store_schema=store_schema)

# Pobranie wszystkich
@app.get("/store_schemas/", response_model=list[schemas.StoreSchema])
async def read_store_schemas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    store_schemas = crud.get_store_schemas(db, skip=skip, limit=limit)
    return store_schemas

# Pobranie po id
@app.get("/store_schemas/{store_schema_id}", response_model=schemas.StoreSchema)
async def read_store_schema(store_schema_id: int, db: Session = Depends(get_db)):
    db_store_schema = crud.get_store_schema(db, store_schema_id=store_schema_id)
    if db_store_schema is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_store_schema