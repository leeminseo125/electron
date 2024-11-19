import io

from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        print(f"Original image size: ({image.size[0]}, {image.size[1]}) pixels")

        return JSONResponse(content={"image height": image.size[0], "image width": image.size[1]})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e)}")
        raise HTTPException(status_code=422, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
