from fastapi import FastAPI, UploadFile, File
from .pdf_parser import extract_text
from .database import SessionLocal, init_db
from .models import Document

init_db()
app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "FastAPI PDF service is running",
        "docs": "/docs"
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    text = extract_text(file_location)
    
    db = SessionLocal()
    doc = Document(filename=file.filename, content=text)
    db.add(doc)
    db.commit()
    db.close()
    
    return {"filename": file.filename, "content_length": len(text)}
