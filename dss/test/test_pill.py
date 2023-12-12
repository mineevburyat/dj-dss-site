from PIL import Image

filename = 'Airplane.bmp'
with Image.open(filename) as image:
    image.load()
    print(image.format, 'формат')
    print(image.size)
    print(image.mode)
    image.show()
