from fastapi import APIRouter, Depends, HTTPException, status

from settings import Settings
from src.services.actor_ofendido import get_datos_actor
from src.user.autenticacion import validate_token

settings = Settings()

router = APIRouter(dependencies=[Depends(validate_token)], tags=["Actores Ofendidos"])


@router.get("/actor_ofendido/{actor_id}", status_code=status.HTTP_200_OK)
async def obtener_actor_por_actor_id(actor_id: str):
    """
    Obtiene los datos de un actor ofendido por su ID de actor.

    Args:
        actor_id (str): ID del actor ofendido.

    Returns:
        dict: Datos del actor ofendido.
    """
    actor_data = get_datos_actor(actor_id)

    if not actor_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Actor ofendido no encontrado"
        )

    return actor_data
