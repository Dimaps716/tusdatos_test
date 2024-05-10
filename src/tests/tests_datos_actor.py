import pytest
from unittest.mock import MagicMock

from fastapi import HTTPException

from src.services.actor_ofendido import get_datos_actor

obtener_actor_ofendido = MagicMock()

def test_get_datos_actor_exito():
    actor_data = "0992339411001"
    obtener_actor_ofendido.return_value = actor_data
    assert get_datos_actor("0968599020001") == actor_data

def test_get_datos_actor_fallo():
    obtener_actor_ofendido.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        get_datos_actor("0968599020001")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Actor no encontrado"
