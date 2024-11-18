# Electron Image Classification Test

## Install 
```bash
conda env create -f environment.yml
```
Download 'yolo11n-cls.pt' in ultralytics model zoo and put it in the backend folder.

```bash
cd frontend
npm install
```
if not run npm, try
```bash
conda install nodejs
```

## Run
#### First Terminal
Start in root directory
```bash
cd backend 
uvicorn server:app --host localhost --port 8000
```

#### Second Terminal
Start in root directory
```bash
cd frontend
npm start
```

## Packaging
Start in root directory
```bash
cd frontend
npm install electron-packager --save-dev
npx electron-packager . MyApp --platform=win32 --arch=x64
```
Packaging option
```bash
# need check about --asar
npx electron-packager . MyApp --platform=win32 --arch=x64 --asar
```

## Run exe File
Start in root directory
```bash
cd backend 
uvicorn server:app --host localhost --port 8000
```
Open & Use exe file while your server is running