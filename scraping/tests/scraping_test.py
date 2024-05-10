from fastapi import HTTPException, status

from scraping.clients.get_detalles_de_procesos import obtener_datos_incidente_judicatura
from scraping.clients.scraping_procesos_judiciales import scraping_procesos


def test_obtener_datos_incidente_judicatura():
    # Prueba positiva
    numero_juicio = ["09332202315769"]
    resultado = obtener_datos_incidente_judicatura(numero_juicio)
    assert len(resultado) == 1
    assert "idJuicio" in resultado[0]

    # Prueba negativa
    numero_juicio = ["123456789"]
    try:
        obtener_datos_incidente_judicatura(numero_juicio)
    except HTTPException as e:
        assert e.status_code == status.HTTP_400_BAD_REQUEST


def test_scraping_procesos_actor_id():
    try:
        actor_id = ["0968599020001"]
        result = scraping_procesos(actor_id=actor_id)
        assert isinstance(result, list)
        assert len(result) > 0

    except Exception as e:
        assert False, f"Error inesperado: {e}"


def test_scraping_procesos_demandado_id():
    try:
        demandado_id = ["1791251237001"]
        result = scraping_procesos(demandado_id=demandado_id)
        assert isinstance(result, list)
        assert len(result) > 0

    except Exception as e:
        assert False, f"Error inesperado: {e}"


def test_scraping_procesos_sin_parametros():
    try:
        result = scraping_procesos()
        assert isinstance(result, list)
        assert len(result) > 0

    except Exception as e:
        assert False, f"Error inesperado: {e}"
