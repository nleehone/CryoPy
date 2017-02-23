from component import *


class LS350Recorder(Recorder):
    def __init__(self):
        super().__init__("LS350")


if __name__ == '__main__':
    with LS350Recorder() as recorder:
        while True:
            pass
