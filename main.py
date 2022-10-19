import io
from math import floor
import os
from PIL import Image
import requests
import pandas as pd
from google.cloud import vision
from google.protobuf.json_format import MessageToDict


clothing_dict_set = {'Hat', 'Shirt', 'Coat', 'Dress', 'Skirt', 'Miniskirt', 'Trousers', 'Jeans', 'Shorts', 'Pants', 'Swimwear', 'Jacket', 'Sweater' }


# returns list of objects with name, bounding box info, and image date
def get_clothing_items(row):
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = row["post_url"]

    response = client.object_localization(image=image)
    try:
        objects = MessageToDict(response._pb)["localizedObjectAnnotations"]
    except KeyError:
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
            obj["uri"] = row["post_url"]
            obj["date"] = row["date"]
            clothing_items.append(obj)

    print(f"{len(clothing_items)} clothing objects detected")

    if len(clothing_items) == 0:
        return None

    return clothing_items
    

def crop_and_get_colors(all_clothes):
    if all_clothes is None:
        return None

    data = []

    for clothing_item in all_clothes:
        uri = clothing_item["uri"]

        response = requests.get(uri)
        img = Image.open(io.BytesIO(response.content))

        try:
            vertices = get_vertices(clothing_item, img)
        except KeyError:
            continue

        clothing_item_image = img.crop(vertices)

        img_byte_arr = io.BytesIO()
        clothing_item_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        rgb = detect_properties_from_image(img_byte_arr)
        clothing_item["rgb"] = rgb

        data.append([clothing_item["name"], clothing_item["date"], clothing_item["uri"], *rgb])

    df = pd.DataFrame(columns=["name", "date", "uri", "r", "g", "b"], data=data)

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


def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "paul-client-secrets.json"
    df = pd.read_csv("data_stuff/data.csv")
    out_fn = "data_sandstorm.csv"

    for i, row in df.iterrows():
        print(f"i:{i}")
        try:
            out_df = pd.read_csv(out_fn)
        except FileNotFoundError:
            # create new dataframe: name, date, uri, r, g, b
            out_df = pd.DataFrame(columns=["name", "date", "uri", "r", "g", "b"])

        items_data = get_clothing_items(row)
        temp_df = crop_and_get_colors(items_data)
        if temp_df is not None:
            out_df = pd.concat([out_df, temp_df])
            out_df.to_csv(out_fn, index=False)


if __name__ == "__main__":
    main()