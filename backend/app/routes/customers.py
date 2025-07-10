from fastapi import APIRouter, Depends, Query
from app.utils.security import get_current_user
from app.services.customers import consultar_clientes

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
