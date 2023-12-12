import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import random

class Example(QWidget):

    def __init__(self, width, height, file):
        super().__init__()
        self.initUI(width, height, file)


    def initUI(self, width, height, file):
        self.file = file
        self.width = width
        self.height = height
        self.setGeometry(300, 300, self.width + 20, self.height + 20)
        self.setWindowTitle('Points')
        self.show()


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()


    def drawPoints(self, qp):
        for h in range(1, self.height):
            for w in range(1, self.width):
                red = hex(int.from_bytes(f.read(1), 'little'))
                green = hex(int.from_bytes(f.read(1), 'little'))
                blue = hex(int.from_bytes(f.read(1), 'little'))
                col = QColor(red, green, blue)
                qp.setPen(col)
                qp.drawPoint(w, h)

if __name__ == '__main__':
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
        bytes_on_pixel = bits_on_pixel // 8 or 1
        # print(bytes_on_pixel, '- байт на пиксель')
        if bytes_on_pixel != 3:
            print('не умею работать побитово')
            exit()
        f.seek(offset, 0)
    
    # for h in range(height):
    #     for w in range(width):
    #         red = hex(int.from_bytes(f.read(1), 'little'))
    #         green = hex(int.from_bytes(f.read(1), 'little'))
    #         blue = hex(int.from_bytes(f.read(1), 'little'))
    #         print(red, green, blue, sep='', end=' ')
    #     print()
        # desktop = QApplication.desktop()
        # x = (desktop.width() - width) // 2
        # y = (desktop.height() - height) // 2
        app = QApplication(sys.argv)
        win_viewer = Example(width, height, f)
        
    
    
    
    
    sys.exit(app.exec_())