from datetime import datetime
from ImageBase64.customError import CustomError

def writeError(text):
    try:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        text_with_time = timestamp + text

        with open('error.txt', 'a', encoding = "utf-8") as error_file:
            error_file.write(text_with_time + '\n')
        # print("Text with timestamp written to error.txt successfully!")
    except Exception as e:
        print(f"Error writing to error.txt: {e}")

def writeLog(text):
    try:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        text_with_time = timestamp + text

        with open('log.txt', 'a', encoding = "utf-8") as log_file:
            log_file.write(text_with_time + '\n')
        # print("Text with timestamp written to log.txt successfully!")
    except Exception as e:
        raise CustomError(f"Error: {e}")
