from pydantic import BaseModel
from typing import List, Dict, Optional

# Schematy używane są w typowaniu zmiennych,
# walidacji typów zmiennych oraz
# oznaczaniu formatu odpowiedzi z API
''' Schematy - Użytkownik
'''
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


''' Schematy - Sklep
'''
class StoreBase(BaseModel):
    name: str

class StoreCreate(StoreBase):
    address: str

class Store(StoreBase):
    id: int
    schema_id: Optional[int]

    class Config:
        orm_mode = True

''' Schematy - Schemat Sklepu
'''
class StoreSchemaBase(BaseModel):
    schema_path: str

class StoreSchemaCreate(StoreSchemaBase):
    store_id: int

class StoreSchema(StoreSchemaBase):
    id: int
    categories: List[str]
    categories_placement: Dict[str, List[int]]

    class Config:
        orm_mode = True