import torch
from torchvision import models, transforms
from PIL import Image
import requests

device = "cuda" if torch.cuda.is_available() else "cpu"


model = models.resnet18(pretrained=True)
model.eval().to(device)

LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_classes = requests.get(LABELS_URL).text.strip().split("\n")

# 이미지 전처리

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.475, 0.456, 0.416],
                         std=[0.225, 0.224, 0.225]),
])

# 이미지 예측
def pre_image(image_path:str):
    image=Image.open(image_path).convert('RGB') # [c, h, w]
    img_trans=transform(image).unsqueeze(0).to(device) # [b, c, h, w]
    with torch.no_grad():
        out=model(img_trans)
        probal=torch.nn.functional.softmax(out, dim=1)[0]
        top_probal, top_class=probal.topk(1)
        return imagenet_classes[top_class.item()], top_probal.item()
