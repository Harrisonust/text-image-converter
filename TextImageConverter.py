import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ascii = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def add_text_to_image(img, text, left, top, text_color=(0, 0, 0), text_size=15):
    if isinstance(img, np.ndarray):  
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    if text in ascii:
        font_text = ImageFont.truetype("font/arial.ttf", text_size)
    else:
        font_text = ImageFont.truetype("font/simsun.ttc", text_size, encoding="utf-8")
    draw.text((left, top), text, text_color, font=font_text)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def convert_word_to_matrix(target_word, rsl):
    img = np.zeros((rsl[0], rsl[1], 1), np.uint8)
    img.fill(255)
    img = add_text_to_image(img, target_word, 0, 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, img = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, rsl)
    return img


while True:
    rsl = (15, 15)
    target_words = input("Texts to be converted: ")

    for target_word in target_words:
        img = convert_word_to_matrix(target_word, rsl)

        for i in range(rsl[0]):
            for j in range(rsl[1]):
                if img[i][j] == 255:
                    print(chr(12288), end='')
                else:
                    print(target_word, end='')
            print()