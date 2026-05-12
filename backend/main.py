from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64
import os
import io

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Görüntü işleme modülleri (her kategori ayrı dosyada)
import renk_format
import geometrik_islemler
import piksel_histogram
import filtreleme_gurultu
import kenar_esikleme
import morfolojik_islemler
import aritmetik_islemler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def read_index():
    with open(os.path.join(frontend_path, "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/histogram")
async def get_histogram(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return JSONResponse(status_code=400, content={"message": "Resim okunamadı."})

        plt.figure(figsize=(6, 4))
        
        # Histogram için gri seviyeye çeviriyoruz
        gray = renk_format.to_grayscale(img)[:,:,0]
        
        # Histogram çizimi (256 bin, 0-255 aralığı)
        plt.hist(gray.ravel(), 256, [0,256], width=1.0)
        plt.xlim([0,256])
            
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        b64_str = base64.b64encode(buf.read()).decode('utf-8')
        return {"histogram_image": f"data:image/png;base64,{b64_str}"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/process")
async def process_image(
    file1: UploadFile = File(...),
    file2: UploadFile = File(None),
    operation: str = Form(...),
    param1: str = Form(None),
    param2: str = Form(None),
    param3: str = Form(None),
    param4: str = Form(None)
):
    try:
        contents = await file1.read()
        nparr = np.frombuffer(contents, np.uint8)
        img1 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img1 is None:
            return JSONResponse(status_code=400, content={"message": "Resim okunamadı."})

        img2 = None
        if file2:
            contents2 = await file2.read()
            nparr2 = np.frombuffer(contents2, np.uint8)
            img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)
            
        processed_img = None
        
        if operation == "gray":
            processed_img = renk_format.to_grayscale(img1)
        elif operation == "binary":
            threshold = int(param1) if param1 else 127
            processed_img = renk_format.to_binary(img1, threshold)
        elif operation == "colorspace_hsv":
            processed_img = renk_format.colorspace_transform_hsv(img1)
        elif operation == "colorspace_ycbcr":
            processed_img = renk_format.colorspace_transform_ycbcr(img1)
            
        elif operation == "rotate":
            angle = int(param1) if param1 else 45
            processed_img = geometrik_islemler.rotate_image(img1, angle)
        elif operation == "crop":
            start_x = int(param1) if param1 else 10
            start_y = int(param2) if param2 else 10
            width = int(param3) if param3 else 200
            height = int(param4) if param4 else 200
            processed_img = geometrik_islemler.crop_image(img1, start_x, start_y, width, height)
        elif operation == "zoom":
            factor = (float(param1) / 100.0) if param1 else 2.0
            processed_img = geometrik_islemler.zoom_image(img1, factor)
            
        elif operation == "hist_stretch":
            processed_img = piksel_histogram.histogram_stretch(img1)
        elif operation == "contrast":
            reduction_percent = float(param1) if param1 else 50.0
            factor = 1.0 - (reduction_percent / 100.0)
            processed_img = piksel_histogram.reduce_contrast(img1, factor)
            
        elif operation == "noise_sp":
            prob = (float(param1) / 100.0) if param1 else 0.05
            processed_img = filtreleme_gurultu.add_salt_and_pepper(img1, prob)
        elif operation == "filter_mean":
            kernel = int(param1) if param1 else 3
            processed_img = filtreleme_gurultu.mean_filter(img1, kernel)
        elif operation == "filter_median":
            kernel = int(param1) if param1 else 3
            processed_img = filtreleme_gurultu.median_filter(img1, kernel)
        elif operation == "filter_motion":
            kernel = int(param1) if param1 else 9
            processed_img = filtreleme_gurultu.motion_filter(img1, kernel)
            
        elif operation == "threshold_double":
            low = int(param1) if param1 else 50
            high = int(param2) if param2 else 150
            processed_img = kenar_esikleme.double_threshold(img1, low, high)
        elif operation == "canny":
            processed_img = kenar_esikleme.canny_edge_detection(img1)
            
        elif operation == "dilate":
            kernel = int(param1) if param1 else 3
            processed_img = morfolojik_islemler.dilate(img1, kernel)
        elif operation == "erode":
            kernel = int(param1) if param1 else 3
            processed_img = morfolojik_islemler.erode(img1, kernel)
        elif operation == "open":
            kernel = int(param1) if param1 else 3
            processed_img = morfolojik_islemler.open_morph(img1, kernel)
        elif operation == "close":
            kernel = int(param1) if param1 else 3
            processed_img = morfolojik_islemler.close_morph(img1, kernel)
            
        elif operation == "arithmetic_sub":
            processed_img = aritmetik_islemler.subtract_images(img1, img2)
        elif operation == "arithmetic_mul":
            processed_img = aritmetik_islemler.multiply_images(img1, img2)
            
        else:
            processed_img = img1

        if processed_img is None:
            processed_img = img1
            
        if processed_img.dtype != np.uint8:
            processed_img = np.clip(processed_img, 0, 255).astype(np.uint8)

        _, encoded_img = cv2.imencode('.png', processed_img)
        b64_str = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
        
        return {"processed_image": f"data:image/png;base64,{b64_str}"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
