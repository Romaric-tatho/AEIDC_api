from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime
from .models import UserRole, DocType

# --- SCHEMAS POUR L'UTILISATEUR ---

class UserBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    pays:str
    numero_telephone:str

class UserCreate(UserBase):
    password: str  # Le mot de passe brut envoyé lors de l'inscription

# Ce que l'utilisateur peut modifier lui-même
class UserUpdateSelf(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    photo_url: Optional[str] = None
    pays: Optional[str] = None
    numero_telephone: Optional[str] = None
    
# Ce que l'ADMIN peut modifier (il hérite de tout + les champs sensibles)
class UserUpdateAdmin(UserUpdateSelf):
    role: Optional[UserRole] = None
    poste_bureau: Optional[str] = None
    expertise_domaine: Optional[str] = None 
    is_active: Optional[bool] = None
    matricule: Optional[str] = None

class UserOut(UserBase):
    id: str
    role: UserRole
    is_active: bool
    date_inscription: datetime
    matricule: Optional[str] = None
    
    class Config:
        from_attributes = True # Permet de convertir les objets SQLAlchemy en Pydantic

# --- SCHEMAS POUR LES TRANSACTIONS ---

class TransactionBase(BaseModel):
    montant: float
    devise: str = "XAF"
    ref_tiers: str

class TransactionOut(TransactionBase):
    id: str
    statut: str
    date_transaction: datetime
    
    class Config:
        from_attributes = True

# --- SCHEMAS POUR LES DOCUMENTS ---

class DocumentOut(BaseModel):
    id: str
    type_doc: DocType
    numero_serie: str
    url_fichier: str
    date_generation: datetime

    class Config:
        from_attributes = True

# --- SCHEMA POUR LE TOKEN (AUTHENTIFICATION) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
