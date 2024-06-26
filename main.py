import image_process
import cv2

import classify
import comp_db

comp_db.init_db()

img = cv2.imread('testdata/ui/dialog-no-border.png')

result = image_process.parse(img.copy(), enable_debug=False)
# print(result)

for row in result:
    print('row =>', row['id'], row['rect'])
    row_img = image_process.crop(img, row['rect'])
    id = row['id']
    image_process.write_output(f'row_img_{id}', row_img, True)
    for cell in row['cells']:
        print('cell =>', cell['id'], cell['rect'])
        cell_img = image_process.crop(img, cell['rect'])
        id = cell['id']
        id = id.replace(':', '__')
        image_process.write_output(f'cell_img_{id}', cell_img, True)

        _, _, feature_vector = classify.parse(f'out/cell_img_{id}.png')
        comp_types = comp_db.query(feature_vector)
        cell['component_type'] = comp_types[0]['name']

print(result)
for row in result:
    for cell in row['cells']:
        x, y, w, h = cell['rect']
        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2,
        )
        cv2.putText(
            img,
            cell['component_type'],
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            1,
        )
image_process.write_output(f'result', img, True)
