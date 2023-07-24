import asyncio
import httpx
from pathlib import Path


async def main():
    image_path = Path.cwd() / r"C:\Users\tmc\Downloads\UNet-MobileNet-Pytorch 4\UNet-MobileNet-Pytorch\000.png"
    # async with httpx.AsyncClient() as client:
    #     response = await client.post("http://192.168.1.100:8080/route")
    #     if response.status_code == 200:
    #         print("请求 route 成功")
    #         routes = list(response.json()["routes"])
    #     else:
    #         print("请求 route 失败")
    #         exit(0)
    async with httpx.AsyncClient() as client:
        with open(image_path, "rb") as file:
            files = {"image": file}
            # data = routes,            data = {"routes": [], "outset": ["localhost:8080"]}
            data = {"routes": ["192.168.3.95:8080"], "outset": ["192.168.3.194:8080"]}
            with open("data.json", "w") as f:
                f.write(str(data))
            # outset = localhost:8080
            response = await client.post(
                "http://localhost:8080/predict", files=files, data=data
            )


            if response.status_code == 200:
                print("请求成功")
            else:
                print("请求失败")
            print(response)


asyncio.run(main())
