from fastapi import HTTPException, status

from db import obtener_actor_ofendido


def get_datos_actor(actor_id):
    """
    Obtiene los datos de un actor por su ID.

    Args:
        actor_id (str): ID del actor.

    Returns:
        dict: Datos del actor.

    Raises:
        HTTPException: Se lanza cuando el actor no se encuentra.
    """

    actor_ofendido = obtener_actor_ofendido(actor_id)

    if actor_ofendido:
        return actor_ofendido
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Actor no encontrado"
        )
