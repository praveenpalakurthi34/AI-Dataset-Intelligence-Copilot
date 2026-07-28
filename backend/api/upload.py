import uuid
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.config import settings
from backend.schemas.dataset import UploadResponse

router = APIRouter(prefix="/api", tags=["Upload"])

@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    # Validate extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension '{file_ext}'. Only .csv files are allowed."
        )

    # Read content to check size
    content = await file.read()
    file_size_bytes = len(content)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if file_size_bytes > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    # Generate unique dataset ID
    dataset_id = str(uuid.uuid4())
    save_path = settings.UPLOAD_FOLDER / f"{dataset_id}.csv"

    # Save file temporarily
    with open(save_path, "wb") as f:
        f.write(content)

    uploaded_at = datetime.utcnow().isoformat()

    return UploadResponse(
        dataset_id=dataset_id,
        filename=file.filename,
        file_size_bytes=file_size_bytes,
        uploaded_at=uploaded_at,
        message="CSV dataset uploaded successfully and ready for analysis."
    )
