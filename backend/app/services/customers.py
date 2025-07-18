from app.database import get_connection
from psycopg2.extras import RealDictCursor

# Constantes de roles
ROLE_SUPER_ADMIN = 1
ROLE_ADMIN = 2
ROLE_SALES = 3
ROLE_LOGISTICS = 4

def filtrar_campos_cliente(cliente: dict, rol_id: int):
    campos_visibles = {
        ROLE_SUPER_ADMIN: cliente,
        ROLE_ADMIN: {
            k: v for k, v in cliente.items()
            if k not in ["identification","created_at", "updated_at", 
                        "user_id_create", "user_id_update"]
        },
        ROLE_SALES: {
            k: v for k, v in cliente.items()
            if k  in [
                "id","name", "address", "email", "mobile",
                "contact_type", "specific_type", "portal_visibility",
                "city", "state", "trade_name"
            ]
        },
        ROLE_LOGISTICS: {
            k: v for k, v in cliente.items()
            if k in [
                "id", "name", "address", "email", "mobile", "city", "state",
                "trade_name", "specific_type"
            ]
        }
    }
    return campos_visibles.get(rol_id, {})


def consultar_clientes(user, page: int = 1, limit: int = 10, contact_type: str = None, search: str = None):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    offset = (page - 1) * limit
    filtros = []
    valores = []

    ##esto puede funcionar para que sales o logistics solo vean ciretos clientes por zona o por sucursal 
    # if user["rol_id"] in [ROLE_SALES, ROLE_LOGISTICS]:
    #     filtros.append("user_id_create = %s")
    #     valores.append(user["id"])  

    if contact_type:
        filtros.append("contact_type ILIKE %s")
        valores.append(contact_type)

    if search:
        filtros.append("(name ILIKE %s OR email ILIKE %s OR identification ILIKE %s)")
        valores += [f"%{search}%"] * 3

    where = f"WHERE {' AND '.join(filtros)}" if filtros else ""

    # Total
    cursor.execute(f"SELECT COUNT(*) FROM customers {where}", valores)
    total = cursor.fetchone()["count"]

    # Datos
    cursor.execute(f"""
        SELECT c.*, 
            u.first_name || ' ' || u.last_name AS managed_by_name
        FROM customers c
        LEFT JOIN users u ON c.user_id_create = u.id_usuario
        {where}
        ORDER BY c.created_at DESC
        LIMIT %s OFFSET %s
    """, valores + [limit, offset])

    rows = cursor.fetchall()
    data = []

    for row in rows:
        cliente = dict(row)
        managed_by_name = cliente.pop("managed_by_name", None)
        cliente["managed_by"] = {
            "user_id": cliente.get("user_id_create"),
            "name": managed_by_name
        }
        cliente_filtrado = filtrar_campos_cliente(cliente, user["rol_id"])
        data.append(cliente_filtrado)

    cursor.close()
    conn.close()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    }

def crear_cliente(data: dict, user: dict):
    conn = get_connection()
    cursor = conn.cursor()

    if user["rol_id"] not in [ROLE_SUPER_ADMIN, ROLE_ADMIN]:
        cursor.close()
        conn.close()
        raise PermissionError("No tienes permisos para crear clientes.")

    query = """
        INSERT INTO customers (
            name, identification, contact_type, address, city, state,
            country, associated_company_id, email, mobile, trade_name,
            specific_type, portal_visibility, user_id_create
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """

    values = [
        data.get("name"),
        data.get("identification"),
        data.get("contact_type"),
        data.get("address"),
        data.get("city"),
        data.get("state"),
        data.get("country"),
        data.get("associated_company_id"),
        data.get("email"),
        data.get("mobile"),
        data.get("trade_name"),
        data.get("specific_type"),
        data.get("portal_visibility"),
        user.get("id")
    ]

    cursor.execute(query, values)
    cliente_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return {"id": cliente_id, "message": "Cliente creado exitosamente"}

def eliminar_cliente(customer_id: int, user: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if user["rol_id"] not in [ROLE_SUPER_ADMIN, ROLE_ADMIN]:
            raise PermissionError("No tienes permisos para eliminar clientes.")

        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        cliente = cursor.fetchone()

        if not cliente:
            raise ValueError("Cliente no encontrado")

        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        conn.commit()

        return {"message": "Cliente eliminado exitosamente"}
    
    finally:
        cursor.close()
        conn.close()