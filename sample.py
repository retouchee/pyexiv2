from pyexiv2 import Image

img = Image(r'.\pyexiv2\tests\1.jpg')
img.read_exif()
img.read_iptc()
img.read_xmp()
img.read_raw_xmp()

img.clear_exif()
img.read_exif()

img.modify_exif({'Exif.Image.Make': 'test-中文-', 'Exif.Image.Rating': ''})
img.read_exif()

dict1 = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
         "Xmp.xmp.Rating": "",
         "Xmp.dc.subject": ["tag1", "tag2", "tag3"]}
img.modify_xmp(dict1)

img.close()



from pyexiv2 import ImageData

with open(r'.\pyexiv2\tests\1.jpg', 'rb') as f:
    with ImageData(f.read()) as img:
        data = img.read_exif()


with open(r'.\pyexiv2\tests\1.jpg', 'rb+') as f:
    with ImageData(f.read()) as img:
        changes = {'Iptc.Application2.ObjectName': 'test'}
        img.modify_iptc(changes)
        f.seek(0)
        f.write(img.get_bytes())
    f.seek(0)
    with ImageData(f.read()) as img:
        result = img.read_iptc()




