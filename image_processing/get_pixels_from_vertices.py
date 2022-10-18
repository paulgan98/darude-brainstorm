from math import floor
from PIL import Image
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=False)


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
