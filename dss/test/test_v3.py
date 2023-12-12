with open('House.bmp', 'rb') as f:
    sign = f.read(2)
    if sign != b'BM':
        print('Это не BMP файл')
        exit(1)
    fsize = int.from_bytes(f.read(4), 'little')
    # смещаем указатель на 4 байта от текущего
    f.seek(4, 1)
    offset = int.from_bytes(f.read(4), 'little')
    header_size = int.from_bytes(f.read(4), 'little')
    width = int.from_bytes(f.read(4), 'little')
    height = int.from_bytes(f.read(4), 'little')
    f.seek(2, 1)
    bits_on_pixel = int.from_bytes(f.read(2), 'little')
    print(fsize, '- размер файла')
    print(offset, '- смещение от начала или местонахождение первого пикселя')
    print(header_size, '- размер заголовка')
    print(width, '- ширина изображения')
    print(height, '- высота изображения')
    print(bits_on_pixel, '- число бит на пиксель')
    bytes_on_pixel = bits_on_pixel // 8 or 1
    print(bytes_on_pixel, '- байт на пиксель')
    if bytes_on_pixel != 3:
        print('не умею работать побитово')
        exit()
    f.seek(offset, 0)
    
    for h in range(height):
        for w in range(width):
            red = hex(int.from_bytes(f.read(1), 'little'))
            green = hex(int.from_bytes(f.read(1), 'little'))
            blue = hex(int.from_bytes(f.read(1), 'little'))
            print(red, green, blue, sep='', end=' ')
        print()
        
    while True:
        chunk = f.read(1)
        if chunk == b'':
            break
        print('Ошибка есть еще непрочитанные пиксели!')
        print(chunk)
