from fastapi import APIRouter
from .Repository import Repository

router = APIRouter()
repository = Repository()

@router.get("/compounds")
async def get_compounds():
    return repository.get_all_compounds()

@router.get("/compounds/colored_by_concentration")
async def get_compounds():
    return repository.get_all_compounds_colored_by_concentration()

@router.get("/compounds/colored_by_moa")
async def get_compounds():
    return repository.get_all_compounds_colored_by_moa()

@router.get("/compound/details/{compound_name}/{compound_concentration}")
async def get_compounds(compound_name: str, compound_concentration: float):
    return repository.get_compound_details(compound_name, compound_concentration)