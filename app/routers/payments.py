from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, auth, database
import httpx # Pour appeler les APIs de FedaPay/Flutterwave

router = APIRouter(
    prefix="/payments",
    tags=["Paiements & Adhésions"]
)

# Simulation des clés API des prestataires (à mettre dans le .env)
FEDAPAY_SECRET_KEY = "votre_cle_fedapay"

@router.post("/verify/{transaction_id}", response_model=schemas.UserOut)
async def verify_and_promote(
    transaction_id: str, 
    current_user: schemas.UserOut = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Route appelée après un paiement réussi sur le site WordPress.
    L'API vérifie le statut chez le prestataire et change le rôle de l'user.
    """
    
    # 1. Appel à l'API du prestataire (Exemple FedaPay)
    # Dans la réalité, on ferait : 
    # response = await httpx.get(f"https://fedapay.com{transaction_id}", headers=...)
    # status_payment = response.json()['status']
    
    # Simulation d'une vérification réussie :
    payment_is_valid = True 
    
    if not payment_is_valid:
        raise HTTPException(status_code=400, detail="La transaction n'a pas pu être vérifiée.")

    # 2. Logique de promotion selon le besoin
    # Imaginons que ce paiement soit pour devenir MEMBRE ACTIF
    updated_user = crud.promote_to_actif(db, user_id=current_user.id)
    
    # 3. Enregistrement de la transaction en base MySQL pour archive
    new_trans = schemas.TransactionBase(
        montant=10000.0, # Exemple : 10.000 FCFA
        ref_tiers=transaction_id,
        devise="XAF"
    )
    crud.create_transaction(db, transaction=new_trans, user_id=current_user.id)

    return updated_user
