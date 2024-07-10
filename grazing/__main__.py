import time 
import datetime
import logging


def main():
    while True: 
        logging.warn(f"hello world {datetime.datetime.now().strftime('%H:%M:%S')}")
        time.sleep(1)


if __name__ == "__main__":
    main()
