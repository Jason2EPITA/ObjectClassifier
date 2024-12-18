from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import torch
from PIL import Image
import io
import cv2

app = FastAPI(title="YOLOv5 Live Classifier")

# Charger le modèle YOLOv5
model_path = "best.pt"
model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True)
model.eval()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint pour prédire les objets dans une image.
    """
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))
    
    # Prédiction
    results = model([img])
    results.render()
    
    # Convertir l'image annotée pour la renvoyer
    annotated_img = Image.fromarray(results.ims[0])
    buf = io.BytesIO()
    annotated_img.save(buf, format="JPEG")
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/jpeg")