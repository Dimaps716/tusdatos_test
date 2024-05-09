import pandas as pd
import requests

from fastapi import BackgroundTasks, status
from db import insertar_datos_actor_ofendido, insertar_datos_demandado_procesado
from scraping.get_detalles_de_procesos import obtener_datos_incidente_judicatura
from setting import Settings

settings = Settings()


def scraping_procesos(actor_id: list = None, demandado_id: list = None):
    """
    Realiza scraping de la página "Consulta de procesos" y guarda los resultados en un archivo CSV.

    Args:
        actor_id (list): Lista de IDs de actores/ofendidos.
        demandado_id (list): Lista de IDs de demandados/procesados.
    """
    try:
        if actor_id:
            filename = "Actor_Ofendido"
            data_type = "actor"
            data_ids = actor_id
        elif demandado_id:
            filename = "Demandado_Procesado"
            data_type = "demandado"
            data_ids = demandado_id
        else:
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar al menos uno de los siguientes parámetros: actor_id, demandado_id",
            )

        url = f"{settings.BASE_URL_API}buscarCausas?page={{}}&size=10"

        all_data = []

        for id in data_ids:
            page = 1
            while True:
                payload = {
                    "numeroCausa": "",
                    "actor": {
                        "cedulaActor": id if data_type == "actor" else "",
                        "nombreActor": "",
                    },
                    "demandado": {
                        "cedulaDemandado": id if data_type == "demandado" else "",
                        "nombreDemandado": "",
                    },
                    "first": page,
                    "numeroFiscalia": "",
                    "pageSize": 10,
                    "provincia": "",
                    "recaptcha": "verdad",
                }
                headers = {
                    "Content-Type": "application/json",
                }

                response = requests.post(
                    url.format(page), headers=headers, json=payload
                )
                data = response.json()

                if not data:
                    break

                all_data.extend(data)
                page += 1
        df = pd.DataFrame(all_data)

        eliminar_columnas_nulas_y_guardar_en_bd(df=df, tabla=filename)
        return all_data
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al realizar el scraping de procesos: {e}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error al realizar el scraping: {e}",
        )


def eliminar_columnas_nulas_y_guardar_en_bd(df, tabla):
    """
    Elimina las columnas nulas de un DataFrame y guarda los datos en la base de datos.

    Args:
        df (pandas.DataFrame): DataFrame con los datos a procesar.
        tabla (str): Nombre de la tabla en la que se guardarán los datos.

    Returns:
        pandas.DataFrame: DataFrame con las columnas nulas eliminadas.
    """
    try:
        df["idMateria"] = df["idMateria"].astype(int)
        df["fechaIngreso"] = pd.to_datetime(df["fechaIngreso"])

        if tabla == "Actor_Ofendido":
            df_data = df.dropna(axis=1)
            insertar_datos_actor_ofendido(df_data)
        else:
            df_data = df.dropna(axis=1, how="all")
            insertar_datos_demandado_procesado(df_data)

        return df_data
    except Exception as e:
        raise RuntimeError(
            f"Error al procesar y guardar los datos en la base de datos: {e}"
        )
