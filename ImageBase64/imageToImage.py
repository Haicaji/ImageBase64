from PIL import Image
import pillow_avif
from os import path
from ImageBase64.customError import *
from ImageBase64.writeLogAndError import writeLog

def imageToImage(o_path, n_path):
    try:
        # 打开原始图片
        img = Image.open(o_path)

        n_suffix = path.splitext(n_path)[1].replace(".", "")

        # 将图片保存为指定格式 n_suffix
        img.save(n_path, format=n_suffix)

        writeLog(f"图片成功转换为 {n_suffix} 格式，并保存至 {n_path}")
    except Exception as e:
        writeLog(f"imageToImage发生错误: {e}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")