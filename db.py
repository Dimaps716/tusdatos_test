import json
import sqlite3

nombre_bd = 'tusdatos.db'

def crear_tabla_demandado_procesado():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Demandado_Procesado (
                id INTEGER PRIMARY KEY,
                idJuicio TEXT,
                estadoActual TEXT,
                idMateria INTEGER,
                nombreDelito TEXT,
                fechaIngreso DATETIME,
                iedocumentoAdjunto TEXT
            )
        ''')

    conn.commit()
    conn.close()


def crear_tabla_actor_ofendido():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Actor_Ofendido (
            id INTEGER PRIMARY KEY,
            idJuicio TEXT,
            estadoActual TEXT,
            idMateria INTEGER,
            nombreDelito TEXT,
            fechaIngreso DATETIME,
            iedocumentoAdjunto TEXT
        )
    ''')
    conn.commit()
    conn.close()


def crear_tabla_proceso():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Proceso (
            idJudicatura TEXT,
            nombreJudicatura TEXT,
            ciudad TEXT,
            idIncidenteJudicatura INTEGER,
            lstIncidenteJudicatura JSON,
            idJuicio TEXT,
            FOREIGN KEY (idJuicio) REFERENCES Demandado_Procesado(idJuicio),
            FOREIGN KEY (idJuicio) REFERENCES Actor_Ofendido(idJuicio)
        )
    ''')

    conn.commit()
    conn.close()


def crear_tabla_detalles_proceso():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Detalles_Proceso (
            id INTEGER PRIMARY KEY,
            codigo INTEGER,
            idJuicio TEXT,
            fecha TEXT,
            tipo TEXT,
            actividad TEXT,
            visible TEXT,
            origen TEXT,
            idMovimientoJuicioIncidente INTEGER,
            ieTablaReferencia TEXT,
            ieDocumentoAdjunto TEXT,
            escapeOut TEXT,
            uuid TEXT,
            alias TEXT,
            nombreArchivo TEXT,
            tipoIngreso TEXT,
            idTablaReferencia TEXT,
            idJudicatura TEXT,
            FOREIGN KEY (idJuicio) REFERENCES Demandado_Procesado(idJuicio),
            FOREIGN KEY (idJuicio) REFERENCES Actor_Ofendido(idJuicio)
        )
    ''')

    conn.commit()
    conn.close()


def insertar_datos_demandado_procesado(datos):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    valores = [(dato.idJuicio, dato.estadoActual, dato.idMateria, dato.nombreDelito,
                dato.fechaIngreso.date(), dato.iedocumentoAdjunto)
               for dato in datos.itertuples(index=False)]

    cursor.executemany('''
                INSERT INTO Demandado_Procesado (idJuicio, estadoActual, idMateria, nombreDelito, fechaIngreso, iedocumentoAdjunto)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', valores)

    conn.commit()
    conn.close()


def obtener_id_juicios_demandado_procesado():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT idJuicio FROM Demandado_Procesado
    ''')
    id_juicios = cursor.fetchall()

    conn.close()

    return [id[0] for id in id_juicios]


def insertar_datos_actor_ofendido(datos):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    valores = [(dato.idJuicio, dato.estadoActual, dato.idMateria, dato.nombreDelito, dato.fechaIngreso.date(),
                dato.iedocumentoAdjunto) for dato in datos.itertuples(index=False)]

    cursor.executemany('''
           INSERT INTO Actor_Ofendido (idJuicio, estadoActual, idMateria, nombreDelito, fechaIngreso, iedocumentoAdjunto)
           VALUES (?, ?, ?, ?, ?, ?)
       ''', valores)
    conn.commit()
    conn.close()

def obtener_id_juicios_actor_ofendido():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT idJuicio FROM Actor_Ofendido
    ''')

    id_juicios = cursor.fetchall()

    conn.close()
    return [id[0] for id in id_juicios]


def insertar_proceso(datos):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    id_judicatura = datos.get("idJudicatura", None)
    nombre_judicatura = datos.get("nombreJudicatura", None)
    ciudad = datos.get("ciudad", None)
    id_incidente_judicatura = datos.get("lstIncidenteJudicatura", [])[0].get("idIncidenteJudicatura", None)
    lst_incidente_judicatura = json.dumps(datos.get("lstIncidenteJudicatura", None))
    idJuicio = datos.get("idJuicio", None)

    cursor.execute('''
        INSERT INTO Proceso (idJudicatura, nombreJudicatura, ciudad, idIncidenteJudicatura, lstIncidenteJudicatura, idJuicio)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_judicatura, nombre_judicatura, ciudad, id_incidente_judicatura, lst_incidente_judicatura, idJuicio))

    conn.commit()
    conn.close()

def insertar_detalles_proceso(datos):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    for dato in datos:
        cursor.execute('''
            INSERT INTO Detalles_Proceso (codigo, idJudicatura, idJuicio, fecha, tipo, actividad, visible, origen, 
                                  idMovimientoJuicioIncidente, ieTablaReferencia, ieDocumentoAdjunto, escapeOut, 
                                  uuid, alias, nombreArchivo, tipoIngreso, idTablaReferencia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (dato['codigo'], dato['idJudicatura'], dato['idJuicio'], dato['fecha'], dato['tipo'], dato['actividad'],
              dato['visible'], dato['origen'], dato['idMovimientoJuicioIncidente'], dato['ieTablaReferencia'],
              dato['ieDocumentoAdjunto'], dato['escapeOut'], dato['uuid'], dato['alias'], dato['nombreArchivo'],
              dato['tipoIngreso'], dato['idTablaReferencia']))

    conn.commit()
    conn.close()

def consultar_por_id_juicio(id_juicio):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM Detalles WHERE idJuicio = ?
    ''', (id_juicio,))

    detalles = cursor.fetchall()

    conn.close()

    return detalles

crear_tabla_demandado_procesado()
crear_tabla_actor_ofendido()
crear_tabla_proceso()
crear_tabla_detalles_proceso()