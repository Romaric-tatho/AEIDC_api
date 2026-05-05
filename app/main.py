from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.routers.users as users


# Création des tables automatiquement au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AEIDC International API",
    description="Système de gestion des membres et certifications",
    version="1.0.0"
)

# Configuration CORS pour WordPress
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # À restreindre plus tard au domaine de l'AEIDC
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Online", "agency": "AEIDC International"}
