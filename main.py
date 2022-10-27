import io
from os import listdir, makedirs
from os.path import isfile, join
from math import floor
import os
from PIL import Image
import pandas as pd
from google.cloud import vision
from google.protobuf.json_format import MessageToDict

rgb_data_fn = "data_sandstorm_new.csv" # output rgb data file name
rgb_data_columns = ["name", "img_name", "r", "g", "b"]
processed_fn = "processed.txt"  # keeps track of images that have already been processed by google cloud vision api
instagram_img_folder = "/Users/PaulG/Downloads/instagram_images"  # full path to instagram image folder
client_secrets_fn = "paul-client-secrets.json"

clothing_dict_set = {'Hat', 'Shirt', 'Coat', 'Dress', 'Skirt', 'Miniskirt', 'Trousers', 'Jeans', 'Shorts', 'Pants', 'Swimwear', 'Jacket', 'Sweater' }


# returns list of objects with name, bounding box info, and image date
def get_clothing_items(img_name):
    client = vision.ImageAnnotatorClient()

    img = Image.open(join(instagram_img_folder, img_name))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_data = img_byte_arr.getvalue()

    image = vision.Image()
    image.content = img_data

    response = client.object_localization(image=image)

    try:
        objects = MessageToDict(response._pb)["localizedObjectAnnotations"]
    except KeyError:
        print("localizedObjectAnnotations not found")
        return None

    clothing_items = []

    # loop through name keys, set is_person to true if Person label is found
    is_person = False
    for obj in objects:
        if obj["name"] == "Person":
            is_person = True
            break
    
    # Person label not found, return None
    if is_person is not True:
        print("Person object not found")
        return None
    
    # loop through objects, if obj is object of interest, we add uri and date info and append to clothing_items
    for obj in objects:            
        if obj["name"] in clothing_dict_set:
            obj["img_name"] = img_name
            clothing_items.append(obj)

    print(f"{len(clothing_items)} clothing objects detected")

    if len(clothing_items) == 0:
        return None

    return clothing_items
    

def crop_and_get_colors(all_clothes):
    if all_clothes is None:
        return None

    data = []

    for i, clothing_item in enumerate(all_clothes):
        img = Image.open(join(instagram_img_folder, clothing_item["img_name"]))

        try:
            vertices = get_vertices(clothing_item, img)
        except KeyError:
            continue

        clothing_item_image = img.crop(vertices)

        img_name = f'{clothing_item["img_name"].split(".")[0]}_{str(i)}.jpg'
        save_cropped_image(clothing_item_image, clothing_item["name"], img_name)

        img_byte_arr = io.BytesIO()
        clothing_item_image.save(img_byte_arr, format='PNG')
        img_data = img_byte_arr.getvalue()

        rgb = detect_properties_from_image(img_data)
        # clothing_item["rgb"] = rgb

        data.append([clothing_item["name"], clothing_item["img_name"], *rgb])

    df = pd.DataFrame(columns=rgb_data_columns, data=data)

    return df
 

def detect_properties_from_image(barr):
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.content = barr

    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    # get the rgb values of the dominant color
    frac_highest, rgb_highest = 0, None
    for color in props.dominant_colors.colors:
        if color.pixel_fraction > frac_highest:
            frac_highest = color.pixel_fraction
            rgb_highest = (int(color.color.red), int(color.color.green), int(color.color.blue))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return rgb_highest


def get_vertices(box, image):
    vertices = box["boundingPoly"]['normalizedVertices']
    # print(vertices[0])
    top_left = get_pixels_from_vertex(vertices[0], image),
    bottom_right = get_pixels_from_vertex(vertices[2], image),
    return [top_left[0][0], top_left[0][1], bottom_right[0][0], bottom_right[0][1]]


def get_pixels_from_vertex(vertex, image):
    x = vertex['x']
    y = vertex['y']
    pixel_x = floor(x * image.width)
    pixel_y = floor(y * image.height)
    return [pixel_x, pixel_y]


def set_img_as_processed(img_name, processed_fn):
    with open(processed_fn, 'r') as f:
        imgs = f.read().splitlines()
        imgs = [x for x in imgs if x != ""]
        imgs.append(img_name)
    with open(processed_fn, 'w') as g:
        for im in imgs:
            g.write(f"{im}\n")


def get_next_unprocessed_img(processed_fn, imgs_folder):
    try:
        with open(processed_fn, 'r') as f:
            imgs = f.read().splitlines()
            imgs = [x for x in imgs if x != ""]
    except:
        _ = open(processed_fn, 'w')
        imgs = []

    all_img_files = get_all_imgs(imgs_folder)
    processed_imgs = set(imgs)

    i = 0
    for f in all_img_files:
        if f not in processed_imgs:
            return f, i
        i += 1

    # else all images processed, exit program
    print("All images processed. Terminating program...")
    exit(0)


# return list of all images in folder
def get_all_imgs(imgs_folder):
    all_img_files = [f for f in listdir(imgs_folder) if isfile(join(imgs_folder, f))] # get all files in folder
    all_img_files = [f for f in all_img_files if f.endswith(('.png', '.jpg', '.jpeg'))] # filter out all image files
    return all_img_files


def save_cropped_image(img, folder, img_name):
    path = join("crops", folder, img_name)
    try:
        img.save(path)
    except FileNotFoundError: # folder does not exist, create empty folder
        makedirs(join("crops", folder))
        img.save(path)


def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = client_secrets_fn
    # df = pd.read_csv("data_stuff/data.csv")

    total_num_images = len(get_all_imgs(instagram_img_folder))
    print(f"{total_num_images} images found. Starting processing...")

    for i in range(total_num_images):
        try:
            out_df = pd.read_csv(rgb_data_fn)
        except FileNotFoundError:
            # create new dataframe: name, img_name, r, g, b
            out_df = pd.DataFrame(columns=rgb_data_columns)

        img_name, ind = get_next_unprocessed_img(processed_fn=processed_fn,
                                            imgs_folder=instagram_img_folder)
        print(f"{ind+1}-\t{img_name}")

        items_data = get_clothing_items(img_name=img_name)
        temp_df = crop_and_get_colors(items_data)
        if temp_df is not None:
            out_df = pd.concat([out_df, temp_df])
            out_df.to_csv(rgb_data_fn, index=False)

        set_img_as_processed(img_name=img_name,
                             processed_fn=processed_fn)


if __name__ == "__main__":
    main()