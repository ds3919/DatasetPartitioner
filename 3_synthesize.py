import pandas as pd
import math
from PIL import Image, ImageOps
import sys
import os

def targetResFinder(imgs):
    length = len(imgs)
    if type(length/2) != int:
        TARGETRES = (imgs.at[length//2, 'resolution'] + imgs.at[(length//2)+1, 'resolution'])/2
    else:
        TARGETRES = imgs.at[length/2, 'resolution']

    return TARGETRES

def squareRes(pixel_count):
    WIDTH = int(math.sqrt(pixel_count))
    return WIDTH

def convertToSquare(img, target_size):
    img = img.convert("RGB")
    width, height = img.size

    if width > target_size or height > target_size:
        left = max((width - target_size) // 2, 0)
        top = max((height - target_size) // 2, 0)
        right = left + target_size
        bottom = top + target_size
        img = img.crop((left, top, right, bottom))

    if img.size[0] < target_size or img.size[1] < target_size:
        delta_w = target_size - img.size[0]
        delta_h = target_size - img.size[1]
        padding = (delta_w // 2, delta_h // 2, delta_w - delta_w // 2, delta_h - delta_h // 2)
        img = ImageOps.expand(img, padding, fill=(255, 255, 255))

    return img


def processImage(input_path, output_path, target_size):
    with Image.open(input_path) as img:
        img = convertToSquare(img, target_size)
        img.save(output_path)


df = pd.read_csv(sys.argv[1]) #path for part
output_directory = sys.argv[2] #output directory
lookup_df = pd.read_csv(sys.argv[3]) #data for each image

os.makedirs(output_directory, exist_ok=True)

df = df.merge(lookup_df, left_on='filename', right_on='new_filename', how='inner')

for row in df.itertuples(index=False):
    processImage(row.image_path, (output_directory+row.filename), squareRes(targetResFinder(df)))

df.to_csv((output_directory+'key.csv'), index=False)
