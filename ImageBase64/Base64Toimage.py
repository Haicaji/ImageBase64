import base64
import imghdr
from os import path
from ImageBase64.writeLogAndError import writeLog
from ImageBase64.dealIni import readIni
from ImageBase64.customError import *
import re

# 将传入的Base64转换为图片
def Base64Toimage(txt_path, image_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            base64_str = file.read()

        get_new_imgae_path = False

        if readIni('Base64ToImage', 'withmarkdown') == 'True':
            # 将二进制数据转换为文本数据
            match = re.match(r'\[(.+)\]:data:image/(.+);base64,(.+)', base64_str)
            if match:
                file_name = match.group(1)  # 获取文件名
                file_type = match.group(2)     # 获取后缀
                base64_str = match.group(3)   # 获取base64编码字符串

                directory_path = path.dirname(image_path)
                image_path = path.join(directory_path, file_name + '.' + file_type)

                get_new_imgae_path = True
        
        # 解码Base64字符串
        img_data = base64.b64decode(base64_str.encode('utf-8'))

        if not get_new_imgae_path:
            # 检测文件类型
            file_type = imghdr.what(None, h=img_data)

            if file_type != None:
                suffix = path.splitext(image_path)[1]
                image_path = image_path.replace(suffix, '.' + file_type)

        # 将图像数据写入文件
        with open(image_path, 'wb') as image_file:
            image_file.write(img_data)

        writeLog(f"图像成功保存至 {image_path}")
    except Exception as e:
        writeLog(f"Base64Toimage()发生错误: {e}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

if __name__ == '__main__':
    Base64Toimage("E:\PythonFile\png-webp-avif-base64\test\4.txt", "E:\PythonFile\png-webp-avif-base64\test-new\4.avif")