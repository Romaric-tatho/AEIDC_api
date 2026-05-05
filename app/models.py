from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime, timezone
import enum

# --- Énumérations pour la cohérence des données ---

class UserRole(str, enum.Enum):
    SIMPLE = "Membre Simple"
    ETUDIANT = "Étudiant"
    ACTIF = "Membre Actif"
    EXPERT = "Expert"
    BUREAU = "Membre Exécutif"
    ADMIN = "Administrateur"

class DocType(str, enum.Enum):
    CARTE_ACTIF = "carte_actif"
    CARTE_EXPERT = "carte_expert"
    CERTIFICAT = "certification"

# --- Tables ---

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nom = Column(String(100))
    prenom = Column(String(100))
    pays = Column(String(100))
    numero_telephone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.SIMPLE)
    is_active = Column(Boolean, default=True)
    date_inscription = Column(DateTime, default=datetime.utcnow)

    # Champs académiques et pro (Nullable selon le rôle)
    matricule = Column(String(50), unique=True, nullable=True) # Pour Etudiants
    expertise_domaine = Column(String(150), nullable=True)     # Pour Experts
    poste_bureau = Column(String(150), nullable=True)          # Pour Bureau Exécutif
    photo_url = Column(String(255), nullable=True)             # Pour Cartes de membres

    # Relations
    transactions = relationship("Transaction", back_populates="owner")
    documents = relationship("Document", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    ref_tiers = Column(String(100), unique=True) # ID FedaPay/Flutterwave
    montant = Column(Float, nullable=False)
    devise = Column(String(10), default="XAF")
    statut = Column(String(20), default="pending") # pending, success, failed
    date_transaction = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="transactions")

class Document(Base):
    __tablename__ = "documents"

    now = datetime.now(timezone.utc) 
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    type_doc = Column(Enum(DocType))
    numero_serie = Column(String(100), unique=True) # ex: AEIDC-CERT-2024-XXX
    url_fichier = Column(String(255))
    date_generation = Column(DateTime, default=now)

    owner = relationship("User", back_populates="documents")
