import httpx
import uvicorn

from typing import List
from loguru import logger
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from pydantic import BaseModel
import sys
import os

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取上级目录的绝对路径
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

# 将上级目录添加到Python解析器的搜索路径中
sys.path.append(parent_dir)

from PIL import Image
from detect import parse_opt,main
import io
import asyncio

from Ours_Run import Run

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
    result: str,
    flag: bool = True,
    # routes: List[str] = [],
    # outset: List[str] = [],

):
    if flag is True:
        print("return to outset successfully", 'result', result, flag)
        return {"code": 200, "msg": "success"}
    else:
        return {"code": 0, "msg": "fail"}


# class scheduleItem(BaseModel):
#     vehicle: List[float] = []
#     num: int
#
# from Importdatabase import mysql
# DataBase = mysql()
#
# @app.post("/schedule")
# async def schedule(
#     # data: List[scheduleItem] = [],
# ):
#     field_data = DataBase.FindAllFieldData()
#     print(field_data)
#
#     vehicles = []
#     nums = []
#     for item in field_data:
#         vehicles.append([item['lat'], item['lng']])
#         nums.append(item['num'])
#
#     if not vehicles:
#         return {'code': 200, "sche_result": []}
#     print(vehicles, nums)
#     sch_result = Run(vehicles, nums)
#     return {'code': 200, "sche_result": sch_result}
#
#
#
#
# @app.post("/update")
# async def updateLoc(
#     data: List[scheduleItem],
# ):
#
#     for item in data:
#         DataBase.UpdateVehicle(item.vehicle[0], item.vehicle[1], item.num)
#
#     return {'code': 200, "sche_result": data}




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
        # 先清空pic文件夹下的receive文件夹
        trans_folder = "/Users/wy/Downloads/vehicle_network-main/yolov5-master/pic/receive"
        if os.path.exists(trans_folder):
            file_list = os.listdir(trans_folder)
            for file_name in file_list:
                file_path = os.path.join(trans_folder, file_name)
                os.remove(file_path)

        #将img保存在pic文件夹下的recvive文件夹下   保存的文件名为vehicle.png
        save_folder = r"C:\Users\tmc\Documents\GitHub\vehicle_network\vehicle_network-main 2\vehicle_network-main\yolov5-master\pic\receive"
        save_filename = "vehicle.png"
        save_path = os.path.join(save_folder, save_filename)
        img.save(save_path)
        print("save successfully")

        # 调用detect.py中的main函数
        opt = parse_opt()
        result = main(opt)
        print('1:', result)

        async with httpx.AsyncClient() as client:
            outset = outset[0]
            print(outset)
            data = result
            with open("data.json", "w") as f:
                f.write(str(data))
            response = await client.post(
                f"http://{outset}/receive",
                # files={"image": (image.filename, image.file, image.content_type)},
                # result = 'ok',
                params={"result": data, "flag": True},
            )


            print(f"http://{outset}/receive")
            if response.status_code != 200:
                logger.warning(f"HTTP Error: {response.status_code}")
                logger.warning(response.json())
            elif response.json().get("code") != 0:
                if response.json().get("data"):
                    logger.warning(response.json().get("data").get("error"))
            else:
                logger.info("Success")
    except Exception as e:
        logger.error(e)
        return {"code": 1, "msg": "failed", "data": {"error": str(e)}}
    return {"code": 0, "msg": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)