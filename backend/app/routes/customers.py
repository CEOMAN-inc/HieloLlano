from fastapi import APIRouter, Depends, Query
from app.utils.security import get_current_user
from app.services.customers import consultar_clientes, crear_cliente
from fastapi import Body, HTTPException

router = APIRouter()

@router.get("/consult", summary="Get all customers with optional filters")
def listar_clientes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    contact_type: str = Query(None),
    search: str = Query(None),
    user = Depends(get_current_user)
):
    return consultar_clientes(user, page, limit, contact_type, search)

@router.post("/create")
def crear_clientes(
    customer: dict = Body(...),
    user = Depends(get_current_user)
):
    try:
        return crear_cliente(customer, user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
