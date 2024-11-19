import io

from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO


app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("yolo11n-cls.pt")

class_dict = {}
with open('imagenet1000_clsidx_to_labels.txt', 'r', encoding='utf-8') as f:
    for _, line in enumerate(f):
        line = line.strip().split(': ')
        class_idx = int(line[0])
        class_name = line[1]
        class_name = class_name[1:-2]
        class_dict[class_idx] = class_name

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    print(f"Original image size: ({image.size[0]}, {image.size[1]}) pixels")
    image = image.resize((224, 224), Image.Resampling.BILINEAR)
    return image

@app.get("/")
async def read_root():
    with open("../frontend/static/index.html", "r", encoding='utf-8') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    try:
        
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        print("File info")
        print(f"Received file: {file.filename}")
        print(f"Content type: {file.content_type}")
        
        image_bytes = await file.read()
        
        print("Start preprocessing image")
        image = preprocess_image(image_bytes)
        
        print("Start model prediction")
        results = model(image)
        
        result = results[0].probs

        print(result.top1)
        print(result.top5)
        print(result.top1conf)
        print(result.top5conf)
        print(class_dict[result.top1])

        top1 = result.top1
        top1conf = round(float(result.top1conf.item()) * 100, 2)

        return JSONResponse(content={"pred_label": top1, "pred_conf": top1conf, "pred_class": class_dict[top1]})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e)}")
        raise HTTPException(status_code=422, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
