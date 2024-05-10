from fastapi import APIRouter, Depends, HTTPException, status

from settings import Settings
from src.services.proceso_detalles import get_proceso_detalle
from src.user.autenticacion import validate_token

settings = Settings()

router = APIRouter(
    dependencies=[Depends(validate_token)], tags=["Consultas de Procesos"]
)


@router.get("/consulta_proceso/{id_juicio}", status_code=status.HTTP_200_OK)
async def consultar_proceso(id_juicio: str):
    """
    Consulta los detalles de un proceso por su ID de juicio.

    Args:
        id_juicio (str): ID del juicio.

    Returns:
        dict: Detalles del proceso.
    """
    proceso_y_detalles = get_proceso_detalle(id_juicio)
    if not proceso_y_detalles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proceso no encontrado"
        )

    return proceso_y_detalles
