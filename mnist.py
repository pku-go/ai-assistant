
# import argparse
# import os
import cv2
import torch
import numpy as np

from lenet import LeNet

def pre_process(img, device):
    img = cv2.resize(img, (28, 28))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img / 255
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img = img.unsqueeze(0)
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img

def inference(model, img):
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    img = pre_process(img, device)
    model.to(device)
    model.eval()
    preds = model(img)
    # preds is the outputs for a batch
    label = preds[0].argmax()
    return label

def image_classification(file):

    model = LeNet(10)
    load_dict = torch.load('lenet.pth')
    model.load_state_dict(load_dict['state_dict'])

    img = cv2.imread(file)
    label = inference(model, img)

    result = label.item()

    return f"Classification result: {result}"

if __name__ == "__main__":
    print(image_classification("mnist.png"))