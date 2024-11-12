from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # 프론트엔드 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("yolo11n-cls.pt")

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
    print("함수 시작")  # 함수 시작 지점 확인
    try:
        print("try 블록 시작")  # try 블록 시작 확인
        
        # 파일이 이미지인지 확인
        if not file.content_type.startswith('image/'):
            print("이미지 파일 아님")  # 이미지 타입 체크
            raise HTTPException(status_code=400, detail="File must be an image")
        
        print("파일 정보:")
        print(f"Received file: {file.filename}")
        print(f"Content type: {file.content_type}")
        
        # 파일 읽기
        print("파일 읽기 시작")
        image_bytes = await file.read()
        print("파일 읽기 완료")
        
        print("이미지 전처리 시작")
        image = preprocess_image(image_bytes)
        print("이미지 전처리 완료")
        print(f"preprocess image type: {type(image)}")
        
        # YOLO 모델 예측
        print("모델 예측 시작")
        results = model(image)
        for r in results:
            print(r.probs)
        print(f"예측 결과: {r.probs}")

        return JSONResponse(content={"prediction": r.probs})
        
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
