import classify

image_class, image_class_id, feature_vector = classify.parse('testdata/resnet/cat.png')
print(image_class, image_class_id, len(feature_vector))
