import io
import os

from google.cloud import vision

client = vision.ImageAnnotatorClient()
file_name = os.path.abspath('IMG_6669.jpeg') #change to URI
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
# image = vision.Image()
# image.source.image_uri = uri

# response = client.label_detection(image=image)
# labels = response.label_annotations
objects = client.object_localization(image=image).localized_object_annotations

# print('Labels:')
# for label in labels: print(label.description)





print('Number of objects found: {}'.format(len(objects)))
for object_ in objects:
    print('\n{} (confidence: {})'.format(object_.name, object_.score))
    print('Normalized bounding polygon vertices: ')
    for vertex in object_.bounding_poly.normalized_vertices:
        print(' - ({}, {})'.format(vertex.x, vertex.y))