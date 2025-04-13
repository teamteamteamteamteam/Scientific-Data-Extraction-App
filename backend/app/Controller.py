from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
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

@router.get("/images/{image_type}/{compound_id}")
async def get_compounds(image_type: str, compound_id: int):
    try:
        blob = repository.get_image_by_type(compound_id, image_type)
        if not blob:
            raise HTTPException(status_code=404, detail="Image not found")
        return Response(content=blob, media_type="image/tiff")
    except ValueError:
            raise HTTPException(status_code=400, detail="Invalid image type")
    
@router.get("/images/png/{image_type}/{compound_id}")
def get_image_as_png(image_type: str, compound_id: int):
    blob = repository.get_image_by_type(compound_id, image_type)
    if not blob:
        raise HTTPException(status_code=404, detail="Image not found")
    
    tiff_image = Image.open(BytesIO(blob))
    png_io = BytesIO()
    tiff_image.save(png_io, format="PNG")
    png_io.seek(0)

    return StreamingResponse(png_io, media_type="image/png")