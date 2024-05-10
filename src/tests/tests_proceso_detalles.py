import pytest
from unittest.mock import MagicMock

from fastapi import HTTPException

from src.services.proceso_detalles import get_proceso_detalle

obtener_proceso = MagicMock()


def test_get_proceso_detalle_exito():
    proceso_data = "12282202406107"
    obtener_proceso.return_value = proceso_data
    assert get_proceso_detalle("12282202406107") == proceso_data

def test_get_proceso_detalle_fallo():
    obtener_proceso.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        get_proceso_detalle("")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Proceso no encontrado"
