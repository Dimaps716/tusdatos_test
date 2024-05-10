import pytest
from unittest.mock import MagicMock

from fastapi import HTTPException

from src.services.demandado_procesado import get_datos_demandado

consultar_demandado_por_demandado_id = MagicMock()

def test_get_datos_demandado_exito():
    demandado_data = "1791251237001"
    consultar_demandado_por_demandado_id.return_value = demandado_data
    assert get_datos_demandado("1791251237001") == demandado_data

def test_get_datos_demandado_fallo():
    consultar_demandado_por_demandado_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        get_datos_demandado("1791251237001")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Demandado no encontrado"
