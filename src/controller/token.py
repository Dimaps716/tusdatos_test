from fastapi import APIRouter, Depends, HTTPException, status

from src.models.user import Token, UserInLogin
from src.user.autenticacion import auth_handler, create_access_token

router = APIRouter(tags=["Autenticación"])


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: UserInLogin = Depends()):
    """
    Autentica al usuario y genera un token de acceso.

    Args:
        form_data (UserInLogin): Datos de inicio de sesión del usuario.

    Returns:
        dict: Token de acceso y tipo de token.
    """
    user = auth_handler.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.get("username")})
    return {"access_token": access_token, "token_type": "bearer"}
