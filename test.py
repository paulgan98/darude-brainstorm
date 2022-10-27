from os import listdir
from os.path import isfile, join

def set_img_as_processed(img_name, fn):
    with open(fn, 'r') as f:
        imgs = f.read().splitlines()
        imgs = [x for x in imgs if x != ""]
        imgs.append(img_name)
    with open(fn, 'w') as g:
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

    processed_imgs = set(x for x in imgs if x != "")
    all_img_files = [f for f in listdir(imgs_folder) if isfile(join(imgs_folder, f))] # get all files in folder
    all_img_files = [f for f in all_img_files if f.endswith(('.png', '.jpg', '.jpeg'))] # filter out all image files

    for f in all_img_files:
        if f not in processed_imgs:
            return f

    # else all images processed, exit program
    print("All files processed")
    exit(0)


processed_fn = "processed.txt"  # keeps track of images that have already been processed by google cloud vision api
instagram_img_folder = "/Users/PaulG/Downloads/instagram_images"  # full path to instagram image folder

for _ in range(2080):
    a = get_next_unprocessed_img(processed_fn, instagram_img_folder)
    set_img_as_processed(a, processed_fn)