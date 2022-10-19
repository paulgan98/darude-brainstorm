import os
from google.cloud import vision

def detect_properties_from_image(barr):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/j/Desktop/work/hackathon/darude-brainstorm/paul-client-secrets.json"
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

    # return 

# def main():
#     img_url = "https://scontent-dfw5-1.cdninstagram.com/v/t51.2885-15/310544112_407943821533673_4992404856792850298_n.jpg?stp=dst-jpg_e15_fr_s1080x1080&_nc_ht=scontent-dfw5-1.cdninstagram.com&_nc_cat=105&_nc_ohc=iFOyUwiaevcAX8s9CpY&edm=ALQROFkBAAAA&ccb=7-5&ig_cache_key=Mjk0NzMwNTQxMTE0OTc5Mjc1Nw%3D%3D.2-ccb7-5&oh=00_AT_aWcsX1a0_CAt-5WQXlUcm5siM7ZtVReliNlAlUeOiKA&oe=6355A320&_nc_sid=30a2ef"
#     detect_properties_uri(img_url)


# if __name__ == "__main__":
#     main()


