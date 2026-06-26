import os
import random
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = 'dataset'
NOISE_ROOT_DIR = 'dataset_noise'

img_size = (100, 100)
digit_size = (20, 50)
digits = ['0', '1', '3', '8']

try:
    font = ImageFont.truetype("arial.ttf", 30)
except IOError:
    font = ImageFont.load_default()

def create_digit_image(digit, direction):
    # пустой холст 100х100
    img = Image.new("L", size=img_size, color=255)

    # изображение цифры 20х50
    digit_img = Image.new("L", size=digit_size, color=255)
    digit_draw = ImageDraw.Draw(digit_img)
    digit_draw.text((0, 0), digit, font=font, fill=0)

    # необходимо ли повернуть
    if direction == 'horizontal':
        digit_img = digit_img.rotate(90, expand=True)

    # предотвращаем возможность выхода цифры за края изображения
    dx, dy = digit_img.size
    max_x = img_size[0] - dx
    max_y = img_size[1] - dy
    
    # генерируем положение цифры
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)

    # соединяем изображения
    img.paste(digit_img, (x, y))
    return img


for digit in digits:
    for i in range(820):
        is_train_sample = i < 800
        direction = "vertical" if i % 2 == 0 else "horizontal"

        sample_type = "train" if is_train_sample else "test_1"
        dir_name = os.path.join(ROOT_DIR, sample_type, digit, direction)
        os.makedirs(dir_name, exist_ok=True)
        filename = f"{digit}_{i}.png"

        img = create_digit_image(digit, direction)
        img.save(os.path.join(dir_name, filename))

noises = {
    "test_2": 20,
    "test_3": 50,
    "test_4": 100,
    "test_5": 200
}

def add_noise(img, pixels_count):
    img_spoiled = img.copy()
    pixels = img_spoiled.load()

    blacked = set()
    # пока не закрасится pixels_count уникальных пикселей
    while len(blacked) < pixels_count:
        # случайная точка на картинке
        x = random.randint(0, img_size[0] - 1)
        y = random.randint(0, img_size[1] - 1)
        
        if (x, y) not in blacked:
            pixels[x, y] = 0
            blacked.add((x, y)) # запоминаем посещенный пиксель
            
    return img_spoiled

for dir_name, pixels_count in noises.items():
    for digit in digits:
        for direction in ['vertical', 'horizontal']:
            # берем исходники из чистого test_1
            source_dir = os.path.join(ROOT_DIR, "test_1", digit, direction)
            
            # сохраняем в отдельную корневую папку dataset_noise
            result_dir = os.path.join(NOISE_ROOT_DIR, dir_name, digit, direction)
            os.makedirs(result_dir, exist_ok=True)

            for filename in os.listdir(source_dir):
                path = os.path.join(source_dir, filename)
                img = Image.open(path)
                img_spoiled = add_noise(img, pixels_count)
                img_spoiled.save(os.path.join(result_dir, filename))
                
print("скрипт выполнен")