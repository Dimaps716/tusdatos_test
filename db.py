import json
import sqlite3

nombre_bd = 'tusdatos.db'


def crear_tabla_usuarios():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')

    conn.commit()
    conn.close()


def crear_tabla_demandado_procesado():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Demandado_Procesado (
                id INTEGER PRIMARY KEY,
                demandado_id TEXT,
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
            actor_id TEXT,
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

    valores = [( dato.demandado_id, dato.idJuicio, dato.estadoActual, dato.idMateria, dato.nombreDelito,
                dato.fechaIngreso.date(), dato.iedocumentoAdjunto)
               for dato in datos.itertuples(index=False)]

    cursor.executemany('''
                INSERT INTO Demandado_Procesado (demandado_id, idJuicio, estadoActual, idMateria, nombreDelito, fechaIngreso, iedocumentoAdjunto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', valores)

    conn.commit()
    conn.close()


def obtener_id_demandado_procesado():
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT demandado_id FROM Demandado_Procesado
    ''')
    demandado = cursor.fetchall()

    conn.close()

    return demandado


def consultar_demandado_por_demandado_id(demandado_id: str):
    conn = sqlite3.connect(nombre_bd)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Demandado_Procesado WHERE demandado_id = ?', (demandado_id,))
    demandados_procesados = cursor.fetchall()

    conn.close()

    demandados_procesados_list = list(map(lambda demandado: dict(demandado), demandados_procesados))

    return demandados_procesados_list


def insertar_datos_actor_ofendido(datos):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    valores = [(dato.actor_id, dato.idJuicio, dato.estadoActual, dato.idMateria, dato.nombreDelito, dato.fechaIngreso.date(),
                dato.iedocumentoAdjunto) for dato in datos.itertuples(index=False)]

    cursor.executemany('''
           INSERT INTO Actor_Ofendido (actor_id, idJuicio, estadoActual, idMateria, nombreDelito, fechaIngreso, iedocumentoAdjunto)
           VALUES (?, ?, ?, ?, ?, ?, ?)
       ''', valores)
    conn.commit()
    conn.close()


def obtener_actor_ofendido(actor_id):
    conn = sqlite3.connect(nombre_bd)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Actor_Ofendido WHERE actor_id = ?', (actor_id,))
    actor_ofendido = cursor.fetchall()

    conn.close()

    actor_ofendido_list = list(map(lambda actor: dict(actor), actor_ofendido))

    return actor_ofendido_list


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


def insertar_usuario(username, password, email):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Usuarios (username, password, email) VALUES (?, ?, ?)', (username, password, email))

    conn.commit()
    conn.close()


def buscar_usuario_email_or_username(email=None, username=None):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()
    if username:
        cursor.execute('SELECT * FROM Usuarios WHERE username = ?', (username,))
    else:
        cursor.execute('SELECT * FROM Usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        return {
            "id": usuario[0],
            "username": usuario[1],
            "password": usuario[2],
            "email": usuario[3]
        }
    else:
        return None
def obtener_proceso(id_juicio: str):
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Proceso WHERE idJuicio = ?', (id_juicio,))
    proceso = cursor.fetchone()
    if not proceso:
        return None
    conn.close()
    return proceso
def obtener_proceso_detalles(id_juicio: str):
    conn = sqlite3.connect(nombre_bd)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Detalles_Proceso WHERE idJuicio = ?', (id_juicio,))
    detalles_proceso = cursor.fetchall()

    conn.close()

    detalles_proceso_list = list(map(lambda detalles: dict(detalles), detalles_proceso))

    return detalles_proceso_list


crear_tabla_demandado_procesado()
crear_tabla_actor_ofendido()
crear_tabla_proceso()
crear_tabla_detalles_proceso()
crear_tabla_usuarios()
