from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/procesar_imagen')
async def procesamiento(image: UploadFile = File(...)):
    image.filename = "imagen.jpg"
    contents = await image.read()

    with open(f"./img/{image.filename}","wb") as f:
        f.write(contents)

    return {"message": "mensaje recibido"}
