from fastapi import HTTPException, status

from db import obtener_proceso, obtener_proceso_detalles


def get_proceso_detalle(id_juicio):
    """
    Obtiene los detalles de un proceso por su ID de juicio.

    Args:
        id_juicio (str): ID del juicio.

    Returns:
        dict: Detalles del proceso.

    Raises:
        HTTPException: Se lanza cuando el proceso no se encuentra.
    """

    proceso = obtener_proceso(id_juicio)

    if not proceso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proceso no encontrado"
        )

    proceso_detalle = obtener_proceso_detalles(id_juicio)

    return {"proceso": proceso, "detalles_proceso": proceso_detalle}
