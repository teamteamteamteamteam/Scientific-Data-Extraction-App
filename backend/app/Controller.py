from fastapi import APIRouter
from .Repository import Repository

router = APIRouter()
repository = Repository()

@router.get("/compounds")
async def get_compounds():
    return repository.get_all_compounds()