import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config.settings import settings # Import our settings

# Global variable to hold the firestore client
db: firestore.Client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    global db
    
    cred_options = {}
    
    # VERCEL DEPLOYMENT WORKFLOW
    # Check if the Vercel environment variables are set
    if settings.firebase_private_key:
        print("Initializing Firebase with Vercel environment variables...")
        # Vercel correctly handles newlines in the private key.
        # We replace escaped newlines with actual newlines, just in case.
        private_key = settings.firebase_private_key.replace('\\n', '\n')
        
        cred_options = {
            'type': 'service_account',
            'project_id': settings.firebase_project_id,
            'private_key_id': '', # Not strictly required by firebase-admin
            'private_key': private_key,
            'client_email': settings.firebase_client_email,
            'client_id': '', # Not strictly required
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': f'https://www.googleapis.com/robot/v1/metadata/x509/{settings.firebase_client_email}'
        }
        cred = credentials.Certificate(cred_options)
        
    # LOCAL DEVELOPMENT WORKFLOW
    # Fallback to local service account file
    elif settings.google_application_credentials:
        print(f"Initializing Firebase with local key: {settings.google_application_credentials}")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
        cred = credentials.ApplicationDefault()
        
    else:
        print("Firebase credentials not found. App may fail to connect.")
        # Allow to proceed for environments that might use ADC (like Google Cloud)
        cred = credentials.ApplicationDefault()


    # Initialize the Firebase app
    try:
        firebase_admin.initialize_app(cred, options={
            'projectId': settings.firebase_project_id,
            'databaseURL': settings.firebase_database_url
        })
        print(f"Firebase App initialized for project: {settings.firebase_project_id}")
    except ValueError as e:
        # This can happen if the app is reloaded
        print(f"Firebase App already initialized: {e}")

    # Initialize the Firestore client
    db = firestore.client()
    
    yield
    # --- Shutdown ---
    pass

app = FastAPI(lifespan=lifespan)

# --- Dependency Injection ---
def get_db() -> firestore.Client:
    return db

bearer_scheme = HTTPBearer()

def get_current_user(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]
) -> dict:
    if not creds:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decoded_token = auth.verify_id_token(creds.credentials)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid ID token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Example Endpoints ---

@app.get("/")
async def root():
    return {"message": f"Hello from Firebase project: {settings.firebase_project_id}"}

@app.get("/items/{item_id}")
async def get_item(
    item_id: str, 
    db_client: Annotated[firestore.Client, Depends(get_db)]
):
    doc_ref = db_client.collection("items").document(item_id)
    doc = await doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Item not found")
    return doc.to_dict()

@app.get("/me")
async def get_protected_data(
    user: Annotated[dict, Depends(get_current_user)]
):
    return {
        "message": "This is protected data!",
        "user_id": user.get("uid"),
        "email": user.get("email"),
    }