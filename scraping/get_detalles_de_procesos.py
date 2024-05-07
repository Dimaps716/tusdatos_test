import requests
import pandas as pd

def obtener_datos_incidente_judicatura(numero_juicio):

    url = f"https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/{numero_juicio}"

    response = requests.get(url)
    data = response.json()

    # Verificar si la respuesta es válida
    if response.status_code == 200:
        # Convertir los datos en un DataFrame de pandas
        df = pd.json_normalize(data)
        return df
    else:
        print("Error al obtener los datos del incidente de la judicatura.")
        return None

    insertar_datos_detalles(data)

    return data


