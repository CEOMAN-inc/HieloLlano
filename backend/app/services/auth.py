from app.database import get_connection
from app.utils.security import hash_password
from app.schemas.user import UserCreate

def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pw = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, hashed_password) VALUES (%s, %s, %s, %s)",
            (user.first_name, user.last_name, user.email, hashed_pw)
        )
        conn.commit()
        return {"first_name": user.first_name, "last_name": user.last_name, "email": user.email}
    except psycopg2.IntegrityError:
        conn.rollback()
        return {"error": "Usuario o email ya registrado"}
    finally:
        cursor.close()
        conn.close()