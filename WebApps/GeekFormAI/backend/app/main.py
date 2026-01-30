from fastapi import FastAPI, UploadFile, File
from .database import SessionLocal, init_db
from .models import Document, DocumentChunk
from .pdf_parser import extract_text
from .embeddings import generate_embedding
from .ai_interpreter import interpret_text

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "GeekForm AI PDF Processor",
        "docs": "/docs"
    }


def chunk_text(text: str, size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"

    # Save uploaded file
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    text = extract_text(file_location)

    # Split into chunks
    chunks = chunk_text(text)

    db = SessionLocal()

    # Store document
    document = Document(
        filename=file.filename,
        content=text
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # Store chunks + embeddings
    for chunk in chunks:
        embedding = generate_embedding(chunk)

        db_chunk = DocumentChunk(
            document_id=document.id,
            chunk_text=chunk,
            embedding=embedding
        )
        db.add(db_chunk)

    db.commit()
    db.close()

    # Optional AI interpretation (DeepSeek-ready)
    interpretation = interpret_text(text[:2000])

    return {
        "filename": file.filename,
        "chunks_stored": len(chunks),
        "ai_interpretation": interpretation
    }
