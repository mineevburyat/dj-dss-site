from PIL import Image

with Image.open('dss/media/emptyphoto.jpg') as i:
    # загрузить в память получиться объект pixel
    p = i.copy()
    mode = i.mode
    format = i.format
print(p)
p.thumbnail((p.width // 3, p.height // 3))
print(p.size, p.mode, p.format)
p.save('thumbnail_medium.png', format)
s = p.copy()
s.thumbnail((s.width // 3, s.height // 3))
s.save('thumbnail_small.png')
