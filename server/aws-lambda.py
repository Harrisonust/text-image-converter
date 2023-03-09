import json

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import boto3

s3_client = boto3.client("s3")
ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def add_text_to_image(img, text, left, top, text_color=(0, 0, 0), text_size=15):
    if isinstance(img, np.ndarray):  
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    
    s3_client.download_file('text-image-converter', "simsun.ttc", "/tmp/simsun.ttc")
    if text in ascii_letters:
        font_text = None
    else:
        font_text = ImageFont.truetype("/tmp/simsun.ttc", text_size, encoding="utf-8")

    draw.text((left, top), text, text_color, font=font_text)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def convert_word_to_matrix(target_word, rsl):
    img = np.zeros((rsl[0], rsl[1], 1), np.uint8)
    img.fill(255)
    img = add_text_to_image(img, target_word, 0, 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, rsl)
    return img

def lambda_handler(event, context):
    rsl = (15, 15)
    

    print(f"{event=}")
    print(f"{context=}")
    
    body = event['body'] # assuming the JSON data is in the "body" field of the event
    
    if body is None:
        target_words = "空"
    else:
        data = json.loads(body)
        target_words = data.get('target', "空")
        
    result = np.empty((len(target_words), 15, 15), int)

    for index, target_word in enumerate(target_words):
        img = convert_word_to_matrix(target_word, rsl)
        
        for i in range(rsl[0]):
            for j in range(rsl[1]):
                if img[i][j] == 255:
                    print(chr(12288), end='')
                    result[index][i][j] = 0
                else:
                    print(target_word, end='') 
                    # result[i][j] = target_word.encode('unicode_escape')
                    result[index][i][j] = 1
            print()
    result = result.tolist()

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
