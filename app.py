from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import uvicorn
from src.utils import get_timestamped_filename, cleanup_old_files

app = FastAPI()

UPLOAD_DIR = Path("images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Generate a timestamp-based filename
        timestamped_filename = get_timestamped_filename(file.filename)
        file_location = UPLOAD_DIR / timestamped_filename
        
        # Save the uploaded file
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Cleanup old files, keeping only the last 4
        cleanup_old_files(UPLOAD_DIR, 4)
        
        return JSONResponse(status_code=200, content={"filename": timestamped_filename})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Run the app with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)