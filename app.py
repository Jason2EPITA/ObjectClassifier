from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import torch
from PIL import Image
import io
import os
import datetime

# Initialiser FastAPI
app = FastAPI(title="YOLOv5 Waste Classifier")
app.mount("/static", StaticFiles(directory="static"), name="static")
# Configurer les templates HTML avec Jinja2
templates = Jinja2Templates(directory="templates")

# Charger le modèle YOLOv5
model_path = "best.pt"
model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True)
model.eval()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Affiche la page d'accueil.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    """
    Endpoint pour classifier les objets dans une image.
    """
    # Lire l'image
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))

    # Effectuer la prédiction
    results = model([img])
    detections = results.pandas().xyxy[0]

    # Annoter l'image
    now_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    output_dir = "static"
    os.makedirs(output_dir, exist_ok=True)
    img_savename = os.path.join(output_dir, f"{now_time}.png")
    results.render()
    Image.fromarray(results.ims[0]).save(img_savename)

    # Extraire les résultats
    predictions = [
        {
            "label": row["name"],
            "confidence": round(float(row["confidence"]) * 100, 2),
            "coordinates": {
                "xmin": round(float(row["xmin"]), 2),
                "ymin": round(float(row["ymin"]), 2),
                "xmax": round(float(row["xmax"]), 2),
                "ymax": round(float(row["ymax"]), 2),
            },
        }
        for _, row in detections.iterrows()
    ]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "image_path": img_savename,
            "predictions": predictions,
        },
    )