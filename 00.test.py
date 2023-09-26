def save_image(image, path):
    image.save(path)

file_name = "new_tst.txt"
with open(f"./images/{file_name}", 'x'): pass