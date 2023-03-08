from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.types import ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

''' Relatywne importy
'''
from .database import Base


''' Model - Użytkownik
'''
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


''' Model - Sklep
'''
class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    schema_id = Column(ForeignKey("store_schemas.id"))


''' Model - Schemat Sklepu
'''
class StoreSchema(Base):
    __tablename__ = "store_schemas"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(ForeignKey("stores.id"))
    categories = ARRAY(String)
    categories_placement = Column(MutableDict.as_mutable(JSONB))
    schema_path = Column(String, unique=True, index=True)