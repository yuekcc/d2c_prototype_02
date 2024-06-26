import os

import numpy as np
from usearch.index import Index, Matches

import classify

DB_NAME = 'index.usearch'

index = Index(
    ndim=2048,  # Define the number of dimensions in input vectors
    metric='cos',  # Choose 'l2sq', 'haversine' or other metric, default = 'ip'
    dtype='f32',  # Quantize to 'f16' or 'i8' if needed, default = 'f32'
    connectivity=16,  # How frequent should the connections in the graph be, optional
    expansion_add=128,  # Control the recall of indexing, optional
    expansion_search=64,  # Control the quality of search, optional
)

LABELS = ['button', 'input', 'select', 'x', 'label']


def init_db():
    index.load(DB_NAME)


def query(feature_vector):
    matches = index.search(feature_vector, 5)
    result = []
    for record in matches:
        result.append(dict(key=record.key, name=LABELS[record.key], distance=record.distance))
    return result


if __name__ == '__main__':
    for i in range(len(LABELS)):
        label = LABELS[i]
        image_class, image_class_id, feature_vector = classify.parse(f'known_ui_components/{label}.png')
        index.add(i, feature_vector)

    index.save(DB_NAME)
