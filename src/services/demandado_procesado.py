from fastapi import HTTPException, status

from db import consultar_demandado_por_demandado_id


def get_datos_demandado(demandado_id):
    """
    Obtiene los datos de un demandado por su ID.

    Args:
        demandado_id (str): ID del demandado.

    Returns:
        dict: Datos del demandado procesado.

    Raises:
        HTTPException: Se lanza cuando el demandado no se encuentra.
    """

    demandado_procesado = consultar_demandado_por_demandado_id(demandado_id)

    if demandado_procesado:
        return demandado_procesado
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Demandado no encontrado"
        )
