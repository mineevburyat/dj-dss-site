with open('113.png', 'rb') as f:
    sign = f.read(2)
    if sign != b'BM':
        print('Это не BMP файл')
        exit(1)
    
    