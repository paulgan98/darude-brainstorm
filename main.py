import io
from math import floor
import os
from PIL import Image
import requests
import pandas as pd
from google.cloud import vision



clothing_dict_set = {'Hat', 'Shirt', 'Coat', 'Dress', 'Skirt', 'Miniskirt', 'Trousers', 'Jeans', 'Shorts', 'Pants', 'Swimwear', 'Jacket', 'Sweater' }

def main():
    df = pd.read_csv("data_stuff/data.csv")

    # create new dataframe: name, date, r, g, b
    out_df = pd.DataFrame(columns=["name", "date", "r", "g", "b"], index=False)

    for row in df.iterrows():
        items_data = get_clothing_items(row)
        temp_df = crop_and_get_colors(items_data)
        out_df = pd.concat([out_df, temp_df])
        
    out_df.to_csv("data_sandstorm.csv", index=False)


# returns list of objects with name, bounding box info, and image date
def get_clothing_items(row):
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = row["post_url"]

    objects = client.object_localization(image=image).localized_object_annotations

    clothing_items = []
    # return 
    
    # loop through name keys, set is_person to true if Person label is found
    is_person = False
    for obj in objects:
        if obj["name"] == "Person":
            is_person = True
            break
    
    # Person label not found, return None
    if is_person is not True: 
        return None
    
    # loop through objects, if obj is object of interest, we add uri and date info and append to clothing_items
    for obj in objects:            
        if obj["name"] in clothing_dict_set:
            obj["uri"] = row["uri"]
            obj["date"] = row["date"]
            clothing_items.append(obj)
        
    return clothing_items
    

def crop_and_get_colors(all_clothes):
    data = []

    for clothing_item in all_clothes:
        uri = clothing_item["uri"]

        response = requests.get(uri)
        img = Image.open(io.BytesIO(response.content))

        vertices = get_vertices(clothing_item, img)
        clothing_item_image = img.crop(vertices)

        img_byte_arr = io.BytesIO()
        clothing_item_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        rgb = detect_properties_from_image(img_byte_arr)
        clothing_item["rgb"] = rgb

        data.append([clothing_item["name"], clothing_item["date"], *rgb])

    df_row = pd.DataFrame(data)
    return df_row
 

def detect_properties_from_image(barr):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../paul-client-secrets.json"
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.content = barr
    # image.source.image_uri = uri

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('frac: {}'.format(color.pixel_fraction))
        print(f"rgb: {(int(color.color.red), int(color.color.green), int(color.color.blue))}")

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return int(color.color.red), int(color.color.green), int(color.color.blue)



def get_vertices(box, image):
    vertices = box["boundingPoly"]['normalizedVertices']
    print(vertices[0])
    top_left     = get_pixels_from_vertex(vertices[0], image),
    bottom_right = get_pixels_from_vertex(vertices[2], image),
    return [top_left[0][0], top_left[0][1], bottom_right[0][0], bottom_right[0][1]]


def get_pixels_from_vertex(vertex, image):
    x = vertex['x']
    y = vertex['y']
    pixel_x = floor(x * image.width)
    pixel_y = floor(y * image.height)
    return [pixel_x, pixel_y]
