import hashlib

from fastapi import HTTPException, status

from db import buscar_usuario_email_or_username, insertar_usuario


def get_usuario_por_correo(email, cosulta: bool = False):
    """
    Obtiene los datos de un usuario por su dirección de correo electrónico.

    Args:
        email (str): Dirección de correo electrónico del usuario.
        consulta (bool, opcional): Indica si es una consulta. Por defecto es False.

    Returns:
        dict: Datos del usuario encontrado.

    Raises:
        HTTPException: Se lanza cuando el usuario no se encuentra y la consulta es False.
    """

    user = buscar_usuario_email_or_username(email=email)

    if user is None and cosulta:
        return None
    elif user:
        return dict(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email no encontrado"
        )


def insertar_usuario_db(user_data):
    """
    Inserta un usuario en la base de datos.

    Args:
        user_data (UserCreate): Datos del usuario a insertar.

    Returns:
        dict: Datos del usuario insertado en la base de datos.
    """
    password_object = hashlib.sha256()
    password_object.update(user_data.password.encode())
    password = password_object.hexdigest()

    user_db = insertar_usuario(
        username=user_data.username, password=password, email=user_data.email
    )

    return user_db
