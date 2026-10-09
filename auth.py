from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

auth_app = FastAPI(
    title="Auth API",
    version="1.0",
    description="Secure authentication API using Supabase Auth and JWT tokens."
)

security = HTTPBearer()

# ── Stage 4: Reusable dependency (replaces per-route token logic) - verify bearer token via supabase.auth.get_user() ──────────────────────────────────────────
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        response = supabase.auth.get_user(token)
        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid or expired token"}
            )
        return response.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"}
        )

# ── Stage 2: Public route (no auth) ──────────────────────────────────────────────────────────────
@auth_app.get("/public/info", summary="Public Info", tags=["Public"])
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# ── Stage 1: Auth routes (signup + login) ───────────────────────────────────────────────────────────────
@auth_app.post("/auth/signup", status_code=status.HTTP_201_CREATED, summary="Sign Up", tags=["Auth"])
def signup(payload: Dict[str, Any]):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail={"error": "Email and password are required"})
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user is None:
            raise HTTPException(status_code=400, detail={"error": "Signup failed"})
        return {"message": "User created successfully", "user": {"id": str(response.user.id), "email": response.user.email}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

@auth_app.post("/auth/login", summary="Log In", tags=["Auth"])
def login(payload: Dict[str, Any]):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail={"error": "Email and password are required"})
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.session is None:
            raise HTTPException(status_code=401, detail={"error": "Invalid login credentials"})
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid login credentials"})

@auth_app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Log Out", tags=["Auth"])
def logout(current_user=Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    return

# ── Stage 2 & 3: Protected routes (bearer token required) ──────────────────────────────────────────────────────────
@auth_app.get("/protected/profile", summary="Get Profile (Protected)", tags=["Protected"])
def get_profile(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "created_at": str(current_user.created_at)
    }

@auth_app.get("/protected/dashboard", summary="Get Dashboard (Protected)", tags=["Protected"])
def get_dashboard(current_user=Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {current_user.email}!",
        "user_id": str(current_user.id)
    }
