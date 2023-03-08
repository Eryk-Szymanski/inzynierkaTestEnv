from sqlalchemy.orm import Session

''' Relatywne importy
'''
from . import models, schemas


# Operacje - Create, Read, Update, Delete
''' Związane z użytkownikiem
'''
# Pobranie po id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Pobranie ze stronicowaniem
# limit strony to 100
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


''' Związane ze sklepem
'''
# Pobranie po id
def get_store(db: Session, store_id):
    return db.query(models.Store).filter(models.Store.id == store_id).first()

def get_store_by_address(db: Session, address: str):
    return db.query(models.Store).filter(models.Store.address == address).first()

# Pobranie ze stronicowaniem
# limit strony to 100
def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).offset(skip).limit(limit).all()

def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(name=store.name, address=store.address)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


''' Związane ze schematem
'''
# Pobranie po id
def get_store_schema(db: Session, store_schema_id):
    return db.query(models.StoreSchema).filter(models.StoreSchema.id == store_schema_id).first()

def get_store_schema_by_store_id(db: Session, store_id):
    return db.query(models.StoreSchema).filter(models.StoreSchema.store_id == store_id).first()

# Pobranie ze stronicowaniem
# limit strony to 100
def get_store_schemas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StoreSchema).offset(skip).limit(limit).all()

def create_store_schema(db: Session, store_schema: schemas.StoreSchemaCreate):
    db_store_schema = models.StoreSchema(schema_path=store_schema.schema_path, store_id=store_schema.store_id)
    db.add(db_store_schema)
    db.commit()
    db.refresh(db_store_schema)
    return db_store_schema