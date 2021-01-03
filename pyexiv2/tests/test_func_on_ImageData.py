# -*- coding: utf-8 -*-
from .base import *


@check_md5
def test_read_all():
    with open(path, 'rb') as f:
        with ImageData(f.read()) as img:
            diff_dict(testdata.EXIF, img.read_exif())
            diff_dict(testdata.IPTC, img.read_iptc())
            diff_dict(testdata.XMP, img.read_xmp())
            assert len(img.read_raw_xmp()) == 4593


def test_modify_exif():
    with open(path, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Exif.Image.ImageDescription': 'test-中文-',
                       'Exif.Image.Artist': ''}
            img.modify_exif(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(testdata.EXIF, changes)
            result = img.read_exif()
            ignored_keys = ['Exif.Image.ExifTag']
            for key in ignored_keys:
                expected_result.pop(key)
                result.pop(key)
            diff_dict(expected_result, result)


def test_modify_iptc():
    with open(path, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Iptc.Application2.ObjectName': 'test-中文-',
                       'Iptc.Application2.Copyright': '',
                       'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3']}
            img.modify_iptc(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(testdata.IPTC, changes)
            diff_dict(expected_result, img.read_iptc())


def test_modify_xmp():
    with open(path, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',
                       'Xmp.xmp.Rating': '',
                       'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']}
            img.modify_xmp(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(testdata.XMP, changes)
            diff_dict(expected_result, img.read_xmp())


def test_clear_all():
    with open(path, 'rb+') as f:
        with ImageData(f.read()) as img:
            img.clear_exif()
            img.clear_iptc()
            img.clear_xmp()
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            assert img.read_exif() == {}
            assert img.read_iptc() == {}
            assert img.read_xmp() == {}


def test_error_log():
    with open(path, 'rb') as f:
        with ImageData(f.read()) as img:
            with pytest.raises(RuntimeError):
                img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
            set_log_level(4)
            img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
            set_log_level(2)    # recover the log level
