#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : 
@Time    : 2018/10/11 15:11
@Describe: 
"""
import qrcode as qrcode

if __name__ == "__main__":
    link = "http://xxxx/test.zip"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=8,
                       border=8, )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image()
    img.save("android_qr_code.png", '')
