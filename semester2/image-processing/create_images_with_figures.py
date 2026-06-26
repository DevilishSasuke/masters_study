import cv2
import numpy as np
import random

width, height = 800, 600
cell_size = 20
padding_size = 2

color_background = (255, 255, 255)
color_square = (255, 0, 0)
color_triangle = (0, 0, 255)

columns = width // cell_size
rows = height // cell_size

def create_canvas():
    return np.ones((height, width, 3), dtype=np.uint8) * 255

def draw_square(img, col, row):
    x1 = col * cell_size + padding_size
    y1 = row * cell_size + padding_size
    x2 = (col + 1) * cell_size - padding_size
    y2 = (row + 1) * cell_size - padding_size
    cv2.rectangle(img, (x1, y1), (x2, y2), color_square, -1)

def draw_triangle(img, col, row):
    x1 = col * cell_size + padding_size
    y1 = row * cell_size + padding_size
    x2 = (col + 1) * cell_size - padding_size
    y2 = (row + 1) * cell_size - padding_size
    
    pts = np.array([[x1, y2], [x2, y2], [x1, y1]], np.int32)
    cv2.fillPoly(img, [pts], color_triangle)

def generate_image_1():
    img = create_canvas()
    sq_cells = [(c, r) for c in range(0, 15) for r in range(rows)]
    tr_cells = [(c, r) for c in range(25, columns) for r in range(rows)]
    
    for c, r in random.sample(sq_cells, 100): draw_square(img, c, r)
    for c, r in random.sample(tr_cells, 100): draw_triangle(img, c, r)
    cv2.imwrite("lab10_img1_easy.png", img)

def generate_image_2():
    img = create_canvas()
    sq_cells = [(c, r) for c in range(0, 20) for r in range(rows)]
    tr_cells = [(c, r) for c in range(20, columns) for r in range(rows)]
    
    for c, r in random.sample(sq_cells, 100): draw_square(img, c, r)
    for c, r in random.sample(tr_cells, 100): draw_triangle(img, c, r)
    cv2.imwrite("lab10_img2_close.png", img)

def generate_image_3():
    img = create_canvas()
    all_cells = [(c, r) for c in range(columns) for r in range(rows)]
    center_zone = [(c, r) for c in range(18, 22) for r in range(10, 20)]
    
    selected_center = random.sample(center_zone, 12)
    sq_center = selected_center[:8]
    tr_center = selected_center[8:]
    
    for c, r in sq_center: draw_square(img, c, r)
    for c, r in tr_center: draw_triangle(img, c, r)
        
    remaining_cells = [cell for cell in all_cells if cell not in center_zone]
    left_pool = [cell for cell in remaining_cells if cell[0] < 18]
    right_pool = [cell for cell in remaining_cells if cell[0] >= 22]
    
    for c, r in random.sample(left_pool, 92): draw_square(img, c, r)
    for c, r in random.sample(right_pool, 96): draw_triangle(img, c, r)
    cv2.imwrite("lab10_img3_overlap.png", img)

generate_image_1()
generate_image_2()
generate_image_3()