import os
import io

from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO


app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.abspath("../frontend/static")), name="static")
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
    return image

@app.get("/")
async def read_root():
    with open("../frontend/static/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    try:
        
        # 파일이 이미지인지 확인
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        print("파일 정보")
        print(f"Received file: {file.filename}")
        print(f"Content type: {file.content_type}")
        
        image_bytes = await file.read()
        
        image = preprocess_image(image_bytes)
        
        # YOLO 모델 예측
        print("모델 예측 시작")
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
        print(f"에러 발생: {str(e)}")
        print(f"에러 타입: {type(e)}")
        raise HTTPException(status_code=422, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import logging
    # 로깅 설정
    logging.basicConfig(level=logging.DEBUG)
    
    uvicorn.run(app, host="localhost", port=5000, log_level="debug")
