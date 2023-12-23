# 配置文件操作
from os import path
import configparser
from ImageBase64.customError import *

def readIni(section, key):
    file_path = "config.ini"

    # 检查ini文件是否存在
    if not path.exists(file_path):
        # 创建默认配置文件
        creatConfigFile(file_path)

        raise CustomError(f"Can't find ini_file: {file_path}.Created default ini_file.")

    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取 INI 文件
    config.read(file_path, encoding="utf-8")

    # 检索指定的键和值
    try:
        value = config.get(section, key)
        return value
    except configparser.NoSectionError:
        raise CustomError(f"未找到节 {section}")
    except configparser.NoOptionError:
        raise CustomError(f"未找到键 {key} 在节 {section}")
    
def creatConfigFile(file_path):
    config_data = {
        'ImageToBase64': {
            '是否添加Markdoown语法': None,
            'addMarkdown': 'True',
            'allinone': 'True',
            'allinonefile': 'allinone.txt',
        },
        'ImageToImage': {
            'defaultformat': 'avif',
        },
        'Base64ToImage': {
            'Base64中是否含有Markdown语法': None,
            'withMarkdown': 'True',
        }
    }

    config = configparser.ConfigParser(allow_no_value=True)

    for section, options in config_data.items():
        config[section] = {}
        for option, value in options.items():
            if value is None:
                config[section][f'; {option}'] = None
            else:
                config[section][option] = str(value)

    with open(file_path, 'w', encoding="utf-8") as configfile:
        config.write(configfile)
        configfile.close()