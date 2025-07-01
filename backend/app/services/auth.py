from app.database import get_connection
from app.utils.security import hash_password, verify_password
from app.schemas.user import UserCreate
import psycopg2

def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pw = hash_password(user.password)
        cursor.execute("""
            INSERT INTO users (first_name, last_name, correo_usuario, hashed_password, estado, rol)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_usuario
        """, (user.first_name, user.last_name, user.email, hashed_pw, True, user.role))

        user_id = cursor.fetchone()[0]

        conn.commit()
        return {
            "id": user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role
        }

    except psycopg2.IntegrityError:
        conn.rollback()
        return {"error": "Usuario ya registrado"}
    finally:
        cursor.close()
        conn.close()

def authenticate_user(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_usuario, first_name, last_name, correo_usuario, hashed_password, estado, rol
            FROM users WHERE correo_usuario = %s
        """, (email,))
        row = cursor.fetchone()
        if row and row[5]:  # estado = True
            id_usuario, first_name, last_name, correo_usuario, hashed_pw, _, rol = row
            if verify_password(password, hashed_pw):
                return {
                    "id": id_usuario,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": correo_usuario,
                    "role": rol
                }
        return None
    finally:
        cursor.close()
        conn.close()
