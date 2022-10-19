import io
from PIL import Image
import sys
from get_pixels_from_vertices import *
from find_bound_boxes import *
from send_cropped_item_for_colors import *


im = Image.open('IMG_6669.jpeg')
# im.show()
def crop_parent_into_children():
    all_clothes = get_all_boxes()
    all_crops = []

    for clothing_item in all_clothes:
        vertices = get_vertices(clothing_item, im)
        clothing_item_image = im.crop(vertices)

        img_byte_arr = io.BytesIO()
        clothing_item_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

    
        all_crops.append(img_byte_arr)
        #send this crop to Vision AI
        # clothing_item_image.show()

    detect_properties_from_image(all_crops[0])

    im.close()