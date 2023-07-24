import asyncio
import io
import uvicorn

from loguru import logger

from fastapi import FastAPI, UploadFile
from PIL import Image
from predict import predict_img, mask_to_image

app = FastAPI()


@app.post("/predict")
async def predict(image: UploadFile):
    """
    Predict liver segmentation on an uploaded image
    """
    try:
        image_data = await image.read()
        img = Image.open(io.BytesIO(image_data))
        mask = await asyncio.get_event_loop().run_in_executor(None, predict_img, img)
        await asyncio.get_event_loop().run_in_executor(None, mask_to_image, mask)
    except Exception as e:
        logger.error(e)
        return {"code": 1, "msg": "failed", "data": {"error": str(e)}}
    return {"code": 0, "msg": "success"}


@app.post("/route")
async def route():
    route_path = []
    # format:
    # ["192.168.1.101:8080", "192.168.1.102:8080", "192.168.1.100:8080"]
    return {"routes": route_path}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
