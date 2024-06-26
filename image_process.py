import cv2
import numpy as np

test_data = 'testdata/ui/dialog-no-border.png'


def write_output(tag: str, img, enable_debug=False):
    if enable_debug:
        cv2.imwrite(f'out/{tag}.png', img)


def into_row_top_bottoms(arr: list[int], threshold=0):
    """
    按阈值进行分组
    """
    result = []
    i = 0
    while i < len(arr):
        if arr[i] == threshold:
            i += 1
            continue
        else:
            start = i
            j = i + 1
            while j < len(arr):
                if arr[j] == threshold:
                    i = j
                    result.append((start, j - 1))
                    break
                else:
                    j += 1
                    continue
    return result


def collect_y_projection(threshold_img: cv2.Mat) -> list[int]:
    """
    图像向 y 轴的投影
    """
    img_height, img_width = threshold_img.shape
    result = []
    for i in range(img_height):
        white_value = 0
        for j in range(img_width):
            if threshold_img[i, j] == 255:
                white_value += 1

        result.append(white_value)
    return result


def collect_x_projection(threshold_img: cv2.Mat) -> list[int]:
    """
    图像向 x 轴的投影
    """
    img_height, img_width = threshold_img.shape

    result = []
    for i in range(img_width):
        white_value = 0
        for j in range(img_height):
            if threshold_img[j, i] == 255:
                white_value += 1
        result.append(white_value)
    return result


def make_projection_image(projection: list[int], image_height: int, image_width: int) -> cv2.Mat:
    """
    创建投影图像
    """
    img = np.zeros((image_height, image_width, 1), np.uint8)
    for i in range(image_height):
        for j in range(projection[i]):
            img[i, j] = 255
    return img


def crop(img: cv2.Mat, rect: tuple[int, int, int, int]):
    x, y, w, h = rect
    return img[y : (y + h), x:w]


def parse(img_path: str, enable_debug=True):
    img = cv2.imread(img_path)
    write_output('input', img, enable_debug)

    h, w, _ = img.shape

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold_img = cv2.threshold(gray_img, 120, 255, cv2.THRESH_BINARY_INV)
    write_output('threshold_img', threshold_img, enable_debug)

    gray_value_x = collect_y_projection(threshold_img)
    hori_projection_img = make_projection_image(gray_value_x, h, w)
    write_output('hori_projection_img', hori_projection_img)

    top_bottoms = into_row_top_bottoms(gray_value_x)
    print('分行区域，每行数据起始位置 Y：', top_bottoms)

    for top_bottom in top_bottoms:
        cv2.rectangle(img, (0, top_bottom[0]), (w, top_bottom[1]), 255, 1)
    write_output('text_rect_x', img, enable_debug)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 3))
    dilate_img = cv2.dilate(threshold_img, kernel)
    write_output('dilate_img', dilate_img, enable_debug)

    result = []
    # 按行分割图片
    for row_index in range(len(top_bottoms)):
        top_bottom = top_bottoms[row_index]

        row = {
            'id': f'{row_index}',
            'cells': [],
            'rect': (0, top_bottom[0], w, top_bottom[1] - top_bottom[0]),  # x, y, w, h
        }

        # cropped = dilate_img[top_bottom[0] : top_bottom[1], 0:w]
        cropped = crop(dilate_img, (0, top_bottom[0], w, top_bottom[1] - top_bottom[0]))
        cropped_height, cropped_width = cropped.shape

        # 垂直投影分割图像
        gray_value_y = collect_x_projection(cropped)
        veri_projection_img = make_projection_image(gray_value_y, cropped_height, cropped_width)
        write_output(f'veri_projection_img {top_bottom}', veri_projection_img, enable_debug)

        left_rights = into_row_top_bottoms(gray_value_y)
        print(f'第 {row_index + 1} 行，left_rights', left_rights)
        for col_index in range(len(left_rights)):
            left_right = left_rights[col_index]
            row['cells'].append(
                {
                    'id': f'{row_index}:{col_index}',
                    'rect': (
                        left_right[0],
                        top_bottom[0],
                        left_right[1] - left_right[0],
                        top_bottom[1] - top_bottom[0],
                    ),  # x, y, w, h
                }
            )

            cv2.rectangle(
                img,
                (left_right[0], top_bottom[0]),
                (left_right[1], top_bottom[1]),
                (0, 0, 255),
                2,
            )
            cv2.putText(
                img,
                f'({row_index + 1}, {col_index + 1})',
                (left_right[0], top_bottom[0]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 0, 255),
                2,
            )
        result.append(row)

    write_output('grid', img, enable_debug)
    return result
