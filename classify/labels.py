import os

LABEL_DATA_FILE = os.path.join(os.path.dirname(__file__), 'synset.txt')

with open(LABEL_DATA_FILE, 'r') as f:
    LABELS = [l.rstrip() for l in f]
