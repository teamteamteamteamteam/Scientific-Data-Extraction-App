from fastapi import APIRouter
from .Repository import Repository
from .Service import Service

router = APIRouter()
repository = Repository()
service = Service()

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

@router.get("/compound/distances/{compound_name}/{compound_concentration}")
async def get_distances_to_compound(compound_name: str, compound_concentration: float):
    return service.get_distances_to_compound(compound_name, compound_concentration)