# import pprint as pp
# from example_response_vision_ai import data
# #import json get json from image parse it and name it data

# def get_all_boxes():
   
#     clothing_dict_set = {'dress', 'shirt', 'hat', 'pants'} # etc

#     objects = data['localizedObjectAnnotations']

#     clothing_objects = []

#     for local_obj in objects:
#         if (local_obj['name']).lower() in clothing_dict_set:
#             clothing_objects.append(local_obj)

#     print("original len: ", len(objects), " ||| clothes only: ", len(clothing_objects))

#     for obj in clothing_objects:
#         pp.pprint(obj)

#     return clothing_objects


