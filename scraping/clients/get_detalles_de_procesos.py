import json
from typing import List

import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException, status

from db import insertar_proceso, insertar_detalles_proceso
from settings import Settings

settings = Settings()


def limpiar_data(data):
    """
    Limpia el texto HTML eliminando etiquetas y espacios adicionales.

    Args:
        data (str): Texto HTML a limpiar.

    Returns:
        str: Texto limpio sin etiquetas HTML y con espacios reducidos.
    """
    actividad_limpia = BeautifulSoup(data, "html.parser").get_text()
    actividad_limpia = " ".join(actividad_limpia.split())
    return actividad_limpia


def obtener_detalles_proceso(data: List[str]) -> List[dict]:
    """
    Obtiene los detalles del proceso judicial y los inserta en la base de datos.

    Args:
        data (dict): Datos del proceso judicial.

    Returns:
        dict: Datos detallados del proceso obtenidos.
    """

    url = f"{settings.BASE_URL_API}EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/actuacionesJudiciales"

    payload = {
        "idMovimientoJuicioIncidente": data["lstIncidenteJudicatura"][0][
            "idMovimientoJuicioIncidente"
        ],
        "idJuicio": data.get("idJuicio"),
        "idJudicatura": data["idJudicatura"],
        "idIncidenteJudicatura": data["lstIncidenteJudicatura"][0][
            "idIncidenteJudicatura"
        ],
        "incidente": 1,
        "nombreJudicatura": data["nombreJudicatura"],
    }
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload)
        )
        data = response.json()

        data_detalles_proceso = []
        for item in data:
            if "actividad" in item:
                item["actividad"] = limpiar_data(item["actividad"])
            data_detalles_proceso.append(item)

        insertar_detalles_proceso(data_detalles_proceso)

        return data

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener datos: {e}",
        )


def obtener_datos_incidente_judicatura(numero_juicio: List[str]) -> List[dict]:
    """
    Obtiene los datos de incidentes de la judicatura para una lista de números de juicio.

    Args:
        numero_juicio (List[str]): Lista de números de juicio.

    Returns:
        List[dict]: Lista de diccionarios con los datos de los incidentes.
    """
    data_response = []

    try:
        for item in numero_juicio:
            url = f"{settings.BASE_URL_API}EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/{item}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data:
                data = data[0]
                data["idJuicio"] = item
                insertar_proceso(data)
                obtener_detalles_proceso(data)
                data_response.append(data)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontraron datos para el número de juicio: {item}",
                )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener datos: {e}",
        )

    return data_response
