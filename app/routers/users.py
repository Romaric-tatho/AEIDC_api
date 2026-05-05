from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import crud, schemas, auth, database

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

# --- ROUTE : INSCRIPTION (SIGNUP) ---

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 1. Vérifier si l'utilisateur existe déjà
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Cet email est déjà enregistré."
        )
    # 2. Créer l'utilisateur (sera 'simple' par défaut)
    return crud.create_user(db=db, user=user)

# --- ROUTE : CONNEXION (LOGIN) ---

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    # 1. Authentifier l'utilisateur
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Générer le jeton JWT
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROUTE : VOIR MON PROFIL (PROTÉGÉE) ---

@router.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user: schemas.UserOut = Depends(auth.get_current_user)):
    """Cette route n'est accessible que si l'utilisateur est connecté"""
    return current_user
