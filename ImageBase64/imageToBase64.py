import base64
from ImageBase64.writeLogAndError import writeLog
from ImageBase64.dealIni import readIni
from os import path

def imageToBase64(image_path, txt_path, suffix = None):
    try:
        with open(image_path, 'rb') as file:
            # 读取图片文件
            image_data = file.read()
            # 将图片数据编码为 Base64 字符串
            base64_str = base64.b64encode(image_data).decode('utf-8')
            if readIni('ImageToBase64', 'addMarkdown') == 'True':
                if suffix is None:
                    suffix = path.splitext(image_path)[1]
                file_name = path.basename(image_path).replace(suffix, '')
                # print(file_name, suffix)
                head_txt = f"[{file_name}]:data:image/{suffix.replace('.', '')};base64,"
            # 将 Base64 字符串写入文本文件
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(head_txt + base64_str)
            # 判断Base64是否需要保存到一起
            if readIni('ImageToBase64', 'allinone') == 'True':
                with open(readIni('ImageToBase64', 'allinonefile'), 'a', encoding='utf-8') as txt_file:
                    txt_file.write(head_txt + base64_str + '\n')

            writeLog(f"图片成功转换为 Base64 字符串，并保存至 {txt_path}")
    except Exception as e:
        writeLog(f"imageToBase64()发生错误: {e}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")