import pandas as pd
from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from scraping.clients.get_detalles_de_procesos import obtener_datos_incidente_judicatura
from scraping.model.scraping_model import ScrapingDataRequest
from scraping.clients.scraping_procesos_judiciales import scraping_procesos
from settings import Settings

settings = Settings()

router = APIRouter(prefix="/Scraping")


@router.post(
    "/scraping",
    tags=["Scraping"],
    status_code=status.HTTP_200_OK,
    summary="Scraping de datos",
    description="Obtiene datos de scraping según los ID de actores y demandados proporcionados.",
)
def scraping_data(data: ScrapingDataRequest, background_tasks: BackgroundTasks):
    """
    Obtiene datos de scraping según los ID de actores y demandados proporcionados.
    """
    if not data.actor_id and not data.demandado_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere al menos un ID de actor o demandado.",
        )

    scraping_procesos_data = scraping_procesos(data.actor_id, data.demandado_id)

    df = pd.DataFrame(scraping_procesos_data)
    data_id = df["idJuicio"].tolist()

    background_tasks.add_task(obtener_datos_incidente_judicatura, data_id)

    return scraping_procesos_data
