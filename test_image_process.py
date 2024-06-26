import image_process
import cv2

img = cv2.imread('testdata/ui/dialog-no-border.png')

result = image_process.parse(img.copy())
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
