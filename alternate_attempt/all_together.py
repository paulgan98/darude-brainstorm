import io, os, csv
from numpy import random
from google.cloud import vision
from PIL import Image
import pandas as pd
import requests

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

filename = "data.csv"

clothing = ["Clothing", "Shorts", "Dress", "Swimwear", "Brassiere", "Tiara", "Shirt", "Coat", "Suit", "Hat", "Fedora",
            "Sun Hat", "Skirt", "Miniskirt", "Fashion accessory", "Glove", "Baseball glove", "Sunglasses", "Sock", "Tie",
            "Goggles", "Cowboy hat", "Sombrero", "Scarf", "Handbag", "Watch", "Umbrella", "Glasses", "Crown", "Swim cap", "Trousers",
            "Jeans", "Footwear", "Roller skates", "Boot", "High heels", "Snadals", "Sports uniform", "Luggage & bags",
            "Backpack", "Suitcase", "Briefcase", "Handbag", "Helmet", "Bicycle helmet", "Football helmet", "Top"]

            

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
     
    # extracting field names through first row
    fields = next(csvreader)
 
    # extracting each data row one by one
    count = 1
    for row in csvreader:
        client = vision.ImageAnnotatorClient()
        image = vision.Image()

        print("TOP OF FOR-LOOP " + str(count))

        image.source.image_uri = row[0]

        # print("Before response")

        response = client.object_localization(image=image)

        # response
        # print("Before localized_object_annotations")

        localized_object_annotations = response.localized_object_annotations

        # print("Before responseURL")

        responseURL = requests.get(row[0])

        # print("Before pillow_image")

        pillow_image = Image.open(io.BytesIO(responseURL.content))

        # print("Before df")

        df = pd.DataFrame(columns=['name', 'score'])

        # print("Before checkForPerson")

        checkForPerson = False
        for obj in localized_object_annotations:
            if obj.name == "Person":
                checkForPerson = True

        if checkForPerson == True:
            print("Person FOUND!!!")
            for obj in localized_object_annotations:
                if obj.name in clothing:
                    print("Clothes FOUND!!!")
                    df = df.append(
                        dict(
                            name=obj.name,
                            score=obj.score
                        ),
                        ignore_index=True)

                    width, height = pillow_image.size

                    box = ((obj.bounding_poly.normalized_vertices[0].x *
                    width, obj.bounding_poly.normalized_vertices[0].y * height,
                    obj.bounding_poly.normalized_vertices[2].x *
                    width, obj.bounding_poly.normalized_vertices[2].y * height))
                    img2 = pillow_image.crop(box)

                    ##############################################################################################################
                    ################ Testing Vision on Sub-Image##################################################################

                    img2.save("Images/"+obj.name+".JPG")
                    img2.show()

                    file_name = obj.name + ".JPG"
                    image_path = os.path.join('.\Images', file_name)

                    with io.open(image_path, 'rb') as image_file:
                        content = image_file.read()

                    image = vision.Image(content=content)
                    response = client.image_properties(image=image).image_properties_annotation

                    response

                    dominant_colors = response.dominant_colors

                    highest_score = dominant_colors.colors[0].score
                    most_dominant_color = dominant_colors.colors[0].color

                    print(highest_score)
                    for itr in dominant_colors.colors:
                        print("Initial highest_score: ")
                        print(highest_score)
                        print("This object's color score:")
                        print(itr.score)
                        if itr.score > highest_score:
                            highest_score = itr.score
                            most_dominant_color = itr.color
                        print("Current highest_score: ")
                        print(highest_score)
                        print("\n")

                    print("THE MOST DOMINANT COLOR")  
                    print(most_dominant_color)
                    print("THE HIGHEST SCORE")
                    print(highest_score)

                    os.remove("Images/"+obj.name+".JPG")

        print("END OF FOR-LOOP " + str(count))
        count += 1
            
                    ##############################################################################################################
