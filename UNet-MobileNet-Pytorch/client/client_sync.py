import httpx
import io
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from PIL import Image

image_path = Path.cwd() / "data/liver/liver/train/000.png"

with open(image_path, "rb") as file:
    files = {"image": file}
    response = httpx.post("http://localhost:80/predict", files=files)

    if response.status_code == 200:
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        plt.imshow(image_array)
        plt.axis("off")
        plt.show()
    else:
        print("请求失败")
