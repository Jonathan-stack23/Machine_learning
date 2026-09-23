"""
Pydantic Schemas para Autenticación y Usuarios
"""
from pydantic import BaseModel, Field
from typing import Optional


class UserLogin(BaseModel):
    username: str = Field(..., description="Nombre de usuario o email", example="inspector")
    password: str = Field(..., min_length=4, description="Contraseña de acceso", example="sena2026")


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, description="Nombre de usuario", example="jonathan_sena")
    email: str = Field(..., description="Correo electrónico", example="inspector@rentacar.com")
    full_name: str = Field(..., description="Nombre completo del inspector", example="Jonathan Inspector SENA")
    password: str = Field(..., min_length=4, description="Contraseña de acceso", example="Sena2026*")
    role: Optional[str] = Field("Inspector", description="Rol del usuario (Inspector, Supervisor, Administrador)")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field("bearer", description="Tipo de token")
    username: str = Field(..., description="Usuario autenticado")
    full_name: str = Field(..., description="Nombre del usuario")
    role: str = Field(..., description="Rol del usuario")


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool = True
