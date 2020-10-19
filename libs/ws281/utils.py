from rpi_ws281x import Color
from .matrix_dict import char2matrix

base_bmp = [0x00000000]  # 一个像素点


def xy_to_array_index(x, y):
    if x % 2 == 0:
        return (x * 8) + y
    else:
        return (x * 8) + (8 - y - 1)


def bmplist2matrix(bmp, width, height):
    """
    将 bmp list 转换为 width 宽 height 高的 matrix
    并将 hex 的颜色转为 10 进制 rgb
    """
    matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            index = x + (y * width)
            color = bmp[index]
            color_r = color >> 24 & 0xFF
            color_g = color >> 16 & 0xFF
            color_b = color >> 8 & 0xFF
            row.append((color_r, color_g, color_b))
        matrix.append(row)

    return matrix


def replace_matrix(base, x, y, data):
    """
    base = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]
    x = 1
    y = 0
    data = [[x],
            [y],
            [z]]

    return [[1, x, 3],
            [4, y, 6],
            [7, z, 9]]
    """

    data_height = len(data)
    data_width = len(data[0])

    for _row in range(data_height):
        for _col in range(data_width):
            base[y + _row][x + _col] = data[_row][_col]

    return base


def render_char(base_matrix, char_list):
    """
    在 base_matrix 上渲染需要的字符

    base_matrix: 生成的 width * height 匹配灯珠阵列的矩阵
    char_list: 要渲染的字符: [(x, y, char)] demo: [(0, 0, 1), (2, 3, 'x')]
    """
    for x, y, char in char_list:
        bmp_data, width, height = char2matrix(char)
        bmp_data_matrix = bmplist2matrix(bmp_data, width, height)
        replace_matrix(base_matrix, x, y, bmp_data_matrix)


def show(strip, matrix, color=None):
    width = len(matrix[0])
    height = len(matrix)
    for row in range(height):
        for col in range(width):
            color_r, color_g, color_b = matrix[row][col]
            _color = Color(color_r, color_g, color_b)
            if (color_r or color_g or color_b) and color:
                _color = color

            strip.setPixelColor(xy_to_array_index(col, row), _color)

    strip.show()
