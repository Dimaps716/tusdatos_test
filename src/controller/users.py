from fastapi import APIRouter, HTTPException, status

from src.models.user import UserCreate, UserInResponse
from src.services.users import get_usuario_por_correo, insertar_usuario_db

router = APIRouter(prefix="/account", tags=["Usuarios"])


@router.post("/users/", response_model=UserInResponse, status_code=status.HTTP_200_OK)
async def create_user(user_data: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        user_data (UserCreate): Datos del usuario a crear.

    Returns:
        dict: Datos del nuevo usuario creado.
    """

    existing_user = get_usuario_por_correo(user_data.email, cosulta=True)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )

    insertar_usuario_db(user_data)

    new_user = get_usuario_por_correo(user_data.email)

    return new_user


@router.get(
    "/users/{email}/", response_model=UserInResponse, status_code=status.HTTP_200_OK
)
async def get_user_by_email(email: str):
    """
    Obtiene los datos de un usuario por su dirección de correo electrónico.

    Args:
        email (str): Dirección de correo electrónico del usuario.

    Returns:
        dict: Datos del usuario.
    """
    user = get_usuario_por_correo(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return user
