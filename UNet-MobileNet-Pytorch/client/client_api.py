import httpx
import uvicorn

from typing import List
from loguru import logger
from fastapi import FastAPI, BackgroundTasks, UploadFile, File

import sys
import os

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取上级目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

# 将上级目录添加到Python解析器的搜索路径中
sys.path.append(parent_dir)

from PIL import Image
from predict import predict_img, mask_to_image
import io
import asyncio

app = FastAPI()


@app.post("/predict")
async def predict(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    routes: List[str] = [],
    outset: List[str] = [],

):
    if not routes:
        print(outset)
        # 如果此时本机的ip和端口等于outset
        # if "192.168.3.149:8080" in outset:
        #     print("return to outset successfully")
        #     return {"code": 0, "msg": "success"}
        # else:
        background_tasks.add_task(predict, image, routes, outset)
        return {"code": 2, "msg": "failed", "data": {"error": "No route available"}}
    background_tasks.add_task(redirect_request, image, routes, outset)
    return {"code": 0, "msg": "success"}

@app.post("/receive")
async def receive(
    # background_tasks: BackgroundTasks,
    result: str = None,
    flag: int = True,
    # routes: List[str] = [],
    # outset: List[str] = [],

):
    if flag == True:
        print("return to outset successfully", 'result', result, flag)
        return {"code": 200, "msg": "success"}
    else:
        return {"code": 0, "msg": "fail"}




async def redirect_request(image: UploadFile, routes: List[str], outset: List[str]):
    logger.info(f"Redirecting request to {routes[0]} with {len(routes)} routes left")
    if not routes:
        return
    async with httpx.AsyncClient() as client:
        route = routes[0]
        routes = routes[1:]
        response = await client.post(
            f"http://{route}/predict",
            files={"image": (image.filename, image.file, image.content_type)},
            data={"routes": routes, "outset": outset},
        )
        if response.status_code != 200:
            logger.warning(f"HTTP Error: {response.status_code}")
            logger.warning(response.json())
        elif response.json().get("code") != 0:
            logger.warning(response.json().get("data").get("error"))
        else:
            logger.info("Success")


async def predict(image: UploadFile, routes: List[str], outset: List[str]):
    """
    Predict liver segmentation on an upload
    """
    try:
        image_data = await image.read()
        img = Image.open(io.BytesIO(image_data))
        mask = await asyncio.get_event_loop().run_in_executor(None, predict_img, img)
        await asyncio.get_event_loop().run_in_executor(None, mask_to_image, mask)
        print("predict successfully")
        async with httpx.AsyncClient() as client:
            outset = outset[0]
            print(outset)
            response = await client.post(
                f"http://{outset}/receive",
                # files={"image": (image.filename, image.file, image.content_type)},
                # result = 'ok',
                data={"result": 'ok', "flag": True },
            )


            print(f"http://{outset}/receive")
            if response.status_code != 200:
                logger.warning(f"HTTP Error: {response.status_code}")
                logger.warning(response.json())
            elif response.json().get("code") != 0:
                logger.warning(response.json().get("data").get("error"))
            else:
                logger.info("Success")
    except Exception as e:
        logger.error(e)
        return {"code": 1, "msg": "failed", "data": {"error": str(e)}}
    return {"code": 0, "msg": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)