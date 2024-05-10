from fastapi import APIRouter, Depends, HTTPException, status

from settings import Settings
from src.services.demandado_procesado import get_datos_demandado
from src.user.autenticacion import validate_token

settings = Settings()

router = APIRouter(
    dependencies=[Depends(validate_token)], tags=["Demandados Procesados"]
)


@router.get("/demandado_procesado/{demandado_id}", status_code=status.HTTP_200_OK)
async def obtener_demandado_por_demandado_id(demandado_id: str):
    demandado_data = get_datos_demandado(demandado_id)

    if not demandado_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demandado procesado no encontrado",
        )

    return demandado_data
