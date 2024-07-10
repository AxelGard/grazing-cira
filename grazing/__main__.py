import time 
import datetime


def main():
    while True: 
        print(f"hello world {datetime.datetime.now().strftime('%H:%M:%S')}")
        time.sleep(1)


if __name__ == "__main__":
    main()
