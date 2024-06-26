import cv2
import numpy as np
from PIL import Image


def load_img(image_path):
    img = Image.open(image_path).convert('RGB')
    return np.array(img)


def parse(image_path):
    img = load_img(image_path)
    img = img / 255.0
    img = cv2.resize(img, (256, 256))
    h, w = img.shape[0], img.shape[1]
    y0 = (h - 224) // 2
    x0 = (w - 224) // 2
    img = img[y0 : y0 + 224, x0 : x0 + 224, :]
    img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    img = np.transpose(img, axes=[2, 0, 1])
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)
    return img
