import os

import numpy as np
import onnxruntime as ort

from . import preprocess_image
from .labels import LABELS

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/resnet50-v2-7__mod.onnx')


def parse(image_path):
    ort_session = ort.InferenceSession(MODEL_PATH)
    image = preprocess_image.parse(image_path)

    input_name = ort_session.get_inputs()[0].name
    output_name = ort_session.get_outputs()[0].name
    feature_layer_name = 'resnetv24_pool1_fwd'  # 特征层的名称，model 文件不同，名称不同
    outputs = ort_session.run([output_name, feature_layer_name], {input_name: image})

    # 输出预测结果
    predictions = outputs[0]  # 假设输出是一个数组，包含了每个类别的概率
    predictions = np.squeeze(predictions)
    predicted_class = np.argsort(predictions)[::-1]

    feature_vector = outputs[1].flatten()
    image_class = LABELS[predicted_class[0]]
    image_class_id = predictions[predicted_class[0]]
    return image_class, image_class_id, feature_vector
