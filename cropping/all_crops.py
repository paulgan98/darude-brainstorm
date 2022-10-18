from PIL import Image
import sys
from IPython.core import ultratb
from crop_clothing import *
from find_bound_boxes import *

sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False)

im = Image.open('/Users/j/Desktop/work/hackathon/IMG_6669.jpeg')
im.show()

all_clothes = get_all_boxes()
all_crops = []

for clothing_item in all_clothes:
    vertices = get_vertices(clothing_item, im)
    clothing_item_image = im.crop(vertices)
    #send this crop to Vision AI
    clothing_item_image.show()


im.close()