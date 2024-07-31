import ImageBase64.Base64Toimage
import ImageBase64.imageToBase64
import ImageBase64.writeLogAndError
import ImageBase64.customError
import ImageBase64.Base64Toimage
import ImageBase64.imageToImage
from ImageBase64.dealIni import readIni
import sys
from os import path, walk, system


def getArgv():
    # 接收传递给可执行文件的参数
    l = len(sys.argv)
    if l == 1:
        print("No parameter was given.")
        system("pause")
        return 0
    # elif l > 2:
    #     raise customError(f"There are too many parameter.")
    else:
        return sys.argv[1:]


def dealFile(file_path, new_file_path=None, suffix=None):
    defaultformat = '.' + readIni('ImageToImage', 'defaultformat')

    # 如果未传入后缀名，获取后缀名
    if suffix is None:
        # 获取文件后缀名
        suffix = path.splitext(file_path)[1]
    # 去后缀名
    file_path = file_path.replace(suffix, '')
    # 如果未传入新文件名，使用原文件名
    if new_file_path is None:
        new_file_path = file_path
    else:
        new_file_path = new_file_path.replace(suffix, '')
    # 处理文件
    # txt -> image
    if suffix == '.txt':
        new_image_path = new_file_path + '.avif'
        # print(new_image_path)
        ImageBase64.Base64Toimage.Base64Toimage(file_path + suffix, new_image_path)
    # avif -> txt
    elif suffix == defaultformat:
        new_txt_path = new_file_path + '.txt'
        # print(new_txt_path)
        ImageBase64.imageToBase64.imageToBase64(file_path + suffix, new_txt_path, suffix)
    # image -> txt
    else:
        new_avif_path = new_file_path + defaultformat
        new_txt_path = new_file_path + '.txt'
        # print(new_avif_path, new_txt_path)
        ImageBase64.imageToImage.imageToImage(file_path + suffix, new_avif_path)
        ImageBase64.imageToBase64.imageToBase64(new_avif_path, new_txt_path, defaultformat)


def dealFolder(folder_path):
    # 遍历文件夹内所有文件和子文件夹
    for root, dirs, files in walk(folder_path):
        # 输出文件的绝对路径
        for file in files:
            file_path = path.join(root, file)
            # 判断是否存在该文件夹
            if not path.exists(path.join(root[-1::-1][::-1] + r"-new")):
                system("mkdir " + path.join(root[-1::-1][::-1] + r"-new"))
            new_file_path = path.join(root[-1::-1][::-1] + r"-new", file)
            suffix = path.splitext(file_path)[1]

            dealFile(file_path, new_file_path=new_file_path, suffix=suffix)
            ImageBase64.writeLogAndError.writeLog(f"         ")


def dealArgv(argv_list):
    for P in argv_list:
        # 获取文件的绝对路径
        P = path.abspath(P)
        # 判断是否存在该文件
        if not path.exists(P):
            ImageBase64.writeLogAndError.writeLog(f"{P} does not exist.\n----------")
            continue
        if path.isfile(P):  # 判断是否为文件
            dealFile(P)
        elif path.isdir(P):  # 判断是否为目录
            dealFolder(P)
        else:
            raise ImageBase64.customError.CustomError(f"dealArgv()Parameter error.")
        ImageBase64.writeLogAndError.writeLog(f"----------")


def main():
    try:
        # 判断allinone是否为True
        if readIni('ImageToBase64', 'allinone') == 'True':
            # 判断allinonefile是否存在
            if path.exists(readIni('ImageToBase64', 'allinonefile')):
                # 删除allinonefile
                system("del " + readIni('ImageToBase64', 'allinonefile'))
        # 获取传入参数
        argv_list = list(getArgv())
        # argv_list = [r".\test"]
        # print(argv_list)
        # 分析参数
        dealArgv(argv_list)
    except Exception as e:
        ImageBase64.writeLogAndError.writeLog(f"Error: {e}")


if __name__ == "__main__":
    main()
