"""
Rutas de Autenticación para FastAPI
"""
from fastapi import APIRouter, HTTPException, Depends, status
from backend.schemas.auth import UserLogin, UserRegister, TokenResponse, UserResponse
from backend.auth.jwt_handler import (
    USERS_DB,
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse, summary="Iniciar Sesión y Obtener JWT")
def login(credentials: UserLogin):
    """
    Autentica a un inspector o administrador y devuelve un Token JWT de acceso.
    - Usuarios por defecto para pruebas:
      - `inspector` / `sena2026`
      - `admin` / `admin123`
    """
    user = USERS_DB.get(credentials.username)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas (usuario o contraseña no válidos)"
        )
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"]
    }


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar Nuevo Inspector")
def register(user_data: UserRegister):
    """
    Registra un nuevo usuario inspector en el sistema.
    """
    if user_data.username in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario '{user_data.username}' ya existe en el sistema"
        )
    
    USERS_DB[user_data.username] = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role or "Inspector",
        "hashed_password": hash_password(user_data.password),
        "is_active": True
    }
    
    return USERS_DB[user_data.username]


@router.get("/me", response_model=UserResponse, summary="Obtener Perfil de Usuario Autenticado")
def get_me(current_user: dict = Depends(get_current_user)):
    """
    Retorna la información del usuario autenticado a través del token JWT en la cabecera.
    """
    return current_user
