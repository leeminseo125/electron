# Electron Image Classification Test

## Install 
```bash
conda create -n electron python=3.11 -y
conda activate electron

pip install -r requirements.txt
```
Download yolo11n-cls.pt in ultralytics model zoo and put it in the backend folder.

```bash
cd frontend
npm install
```

## Run
#### First Terminal
Start in root directory
```bash
cd backend 
uvicorn server:app --host localhost --port 5000
```

#### Second Terminal
Start in root directory
```bash
cd frontend
npm start
```
