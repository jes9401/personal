
import logging

if __name__ == '__main__':
    mylogger = logging.getLogger("my")
    mylogger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s -%(levelname)s - %(message)s")

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    mylogger.addHandler(stream_hander)

    file_handler = logging.FileHandler('my.log')
    mylogger.addHandler(file_handler)

    mylogger.info("server start!!!")