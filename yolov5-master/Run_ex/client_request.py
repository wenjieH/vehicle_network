import asyncio
import httpx
from pathlib import Path
from Ours_Run import Run
from detect import parse_opt,main

vehicles_ip = ["192.168.3.241:8080"]
servers_ip = ["192.168.3.194:8080"]
async def main():
    image_path = Path.cwd() / r"C:\Users\tmc\Documents\GitHub\vehicle_network\vehicle_network-main 2\vehicle_network-main\yolov5-master\pic\trans\vehicle.png"
    # async with httpx.AsyncClient() as client:
    #     response = await client.post("http://192.168.1.100:8080/route")
    #     if response.status_code == 200:
    #         print("请求 route 成功")
    #         routes = list(response.json()["routes"])
    #     else:
    #         print("请求 route 失败")
    #         exit(0)
    async with httpx.AsyncClient() as client:
        the_id = 0

        with open(image_path, "rb") as file:
            files = {"image": file}
            # data = routes,            data = {"routes": [], "outset": ["localhost:8080"]}
            data = {"routes": ["192.168.3.194:8080"], "outset": ["192.168.3.194:8080"]}
            schedule_response = await client.post(
                "http://192.168.3.194:8080/schedule", files=files, data=data
            )
            routes = []
            if schedule_response[the_id][1] != -1:
                route_sch = schedule_response[0][0]

                for item in route_sch[:-1]:
                    routes.append(vehicles_ip[item])

                routes.append(servers_ip[schedule_response[the_id][1]])

                data = {"routes": routes, "outset": [servers_ip[schedule_response[the_id][1]]]}

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

            else:
                opt = parse_opt()
                result = main(opt)
                print(result)
                pass







asyncio.run(main())
