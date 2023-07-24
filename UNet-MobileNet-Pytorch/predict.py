import logging

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from mobilenet.UNet_MobileNet import UNet

from utils.dataset import BasicDataset
from utils.data_vis import plot_img_and_mask


model = r"C:\Users\tmc\Downloads\UNet-MobileNet-Pytorch 4\UNet-MobileNet-Pytorch\data\liver\checkpoints\MobileNet_UNet_epoch91.pt"

net = UNet(n_channels=3, num_classes=1)
logging.info("Loading model {}".format(model))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logging.info(f"Using device {device}")
net.to(device=device)
net.load_state_dict(torch.load(model, map_location=device))
logging.info("Model loaded !")


def predict_img(
    full_img: Image.Image,
    net: UNet = net,
    device: torch.device = device,
    scale_factor: float = 1.0,
    out_threshold: float = 0.5,
) -> np.ndarray:
    net.eval()

    img = torch.from_numpy(BasicDataset.preprocess(full_img, scale_factor))
    img = img.unsqueeze(0)
    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = net(img)

        if net.num_classes > 1:
            probs = F.softmax(output, dim=1)
        else:
            probs = torch.sigmoid(output)

        probs = probs.squeeze(0)

        tf = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize(full_img.size[1]),
                transforms.ToTensor(),
            ]
        )

        probs = tf(probs.cpu())
        full_mask = probs.squeeze().cpu().numpy()

    return full_mask > out_threshold


def mask_to_image(mask):
    return Image.fromarray((mask * 255).astype(np.uint8))


if __name__ == "__main__":
    fn = "data/liver/liver/train/000.png"
    logging.info("\nPredicting image {} ...".format(fn))
    img = Image.open(fn)
    mask = predict_img(
        net=net,
        full_img=img,
        device=device,
    )

    result = mask_to_image(mask)
    plot_img_and_mask(img, mask)
