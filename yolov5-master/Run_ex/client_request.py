import asyncio
import httpx
from pathlib import Path
from Ours_Run import Run
from detect import parse_opt, main
import json

vehicles_ip = ["192.168.1.105:8080", "192.168.1.113:8080", "192.168.1.109:8080", "192.168.1.107:8080", "192.168.1.106:8080", "192.168.1.108:8080", "192.168.1.110:8080", "192.168.1.112:8080", "192.168.1.111:8080"]
servers_ip = ["192.168.1.101:8080"]
flag = 0
async def execute():
    image_path = Path.cwd() / r"E:\vehicle_network\vehicle_network\yolov5-master\pic\receive\vehicle.png"
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
            # data = {"routes": ["192.168.3.194:8080"], "outset": ["192.168.3.194:8080"]}
            schedule_response = await client.post(
                "http://192.168.3.194:8080/schedule"
            )

            print('schedule_response:', json.loads(schedule_response.content))
            schedule_response = json.loads(schedule_response.content)['sche_result']
            print('schedule_response:', schedule_response)
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
                flag = 1
                opt = parse_opt()
                result = main(opt)
                print(result)
                # pass



asyncio.run(execute())
# if flag == 1:
#     opt = parse_opt()
#     result = main(opt)
#     print(result)