
from app_news.models import ImageMedia
from django.core.management.base import BaseCommand
from io import BytesIO
from django.core.files.base import ContentFile
from pathlib import Path
from PIL import Image as PImage
from django.db.models.signals import post_save
from django.dispatch import receiver



class Command(BaseCommand):
    help = 'Генерирует миниатюры с разными размерами, для тех экземпляров медиабиблиотеки, у которых нет миниатюр'
    def handle(self, *args, **kwargs):
        THUMBNAIL = 150
        MEDIUM = 320
        LARGE = 1080
        thumb_images = {
            'large': LARGE,
            'medium': MEDIUM,
            'thumbnail': THUMBNAIL
        }
        images = ImageMedia.objects.all()
        for image in images:
            # image.image.open()
            try:
                img_f = PImage.open(image.image)
            except:
                print(f"Warning! {image} not found!!")
                continue
            img_format = img_f.format
            exten = Path(image.image.name).suffix[1:]
            fname = Path(image.image.name).stem
            # print(f'full {image.pk}:', image.get_img_size(), image.get_fsize(), image.image.name)
            # сгенерировать миниатюры
            for field, im_size in thumb_images.items():
                inst_attr = getattr(image, field)
                if inst_attr == '':
                    if image.width > im_size:
                        percent = im_size / image.width
                        new_hight = int(image.height * percent)
                        img_resize = img_f.resize((im_size, new_hight))
                    else:
                        img_resize = img_f.copy()
                    prefix = field[0]
                    newfilename = f"{prefix}_{fname}.{exten}"
                    file_bufer = BytesIO()
                    img_resize.save(file_bufer, img_format)
                    file_bufer.seek(0)
                    inst_attr.save(
                            newfilename,
                            ContentFile(file_bufer.read()),
                            save=True)
                    img_f_size = file_bufer.getbuffer().nbytes
                    file_bufer.close()
                    inst_attr.close()
                    print('создано: ', field, img_resize.size, img_f_size, inst_attr.name)
                    image.save()
                else:
                    try:
                        img_f_mini = PImage.open(inst_attr)
                        img_f_mini.close()
                    except:
                        print(inst_attr, 'not found!')
                        if image.width > im_size:
                            percent = im_size / image.width
                            new_hight = int(image.height * percent)
                            img_resize = img_f.resize((im_size, new_hight))
                        else:
                            img_resize = img_f.copy()
                        prefix = field[0]
                        newfilename = f"{prefix}_{fname}.{exten}"
                        file_bufer = BytesIO()
                        img_resize.save(file_bufer, img_format)
                        file_bufer.seek(0)
                        inst_attr.save(
                            newfilename,
                            ContentFile(file_bufer.read()),
                            save=True)
                        img_f_size = file_bufer.getbuffer().nbytes
                        file_bufer.close()
                        inst_attr.close()
                        print('создано: ', field, img_resize.size, img_f_size, inst_attr.name)
            img_f.close()            
        
