<<<<<<< Updated upstream
=======
from sqlalchemy.orm import Session
from . import models, schemas, auth
import uuid

# --- GESTION DES UTILISATEURS ---

def get_user_by_email(db: Session, email: str):
    """Vérifie si un email existe déjà dans la base"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Inscrit un nouvel utilisateur simple"""
    hashed_pwd = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        password_hash=hashed_pwd,
        nom=user.nom,
        prenom=user.prenom,
        pays=user.pays,
        numero_telephone=user.numero_telephone,
        role=models.UserRole.SIMPLE,
        photo_url=user.photo_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, user_update: schemas.UserUpdateAdmin):
    """Met à jour les informations d'un utilisateur (admin ou lui-même)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    
    # Mise à jour des champs modifiables
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

# --- GESTION DES TRANSACTIONS ---

def create_transaction(db: Session, transaction: schemas.TransactionBase, user_id: str):
    """Enregistre une tentative de paiement"""
    db_trans = models.Transaction(
        **transaction.model_dump(),
        user_id=user_id,
        statut="pending"
    )
    db.add(db_trans)
    db.commit()
    db.refresh(db_trans)
    return db_trans

def update_transaction_status(db: Session, transaction_id: str, status: str):
    """Met à jour le statut après confirmation du service de paiement"""
    db_trans = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_trans:
        db_trans.statut = status
        db.commit()
    return db_trans

# --- LOGIQUE DE PROMOTION (Changement de rôle) ---

def promote_to_actif(db: Session, user_id: str):
    """Passe un utilisateur au statut Membre Actif"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.role = models.UserRole.ACTIF
        db.commit()
    return user

def promote_to_etudiant(db: Session, user_id: str):
    """Passe un utilisateur au statut Etudiant et génère son matricule"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.role = models.UserRole.ETUDIANT
        # Génération matricule simple : AEIDC + Année + 4 derniers chiffres de l'ID
        import datetime
        year = datetime.datetime.now().year
        suffix = user.id[-4:]
        user.matricule = f"AEIDC-{year}-{suffix}".upper()
        db.commit()
    return user
>>>>>>> Stashed changes
