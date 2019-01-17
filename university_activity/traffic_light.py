from time import sleep
from enum import Enum


class Light(Enum):
    RED = 'Red'
    YELLOW = 'Yellow'
    GREEN = 'Green'

    def __str__(self):
        return f'{self.value}'


class TrafficLight(object):
    DEFAULT_SWITCH_TIME_SECS: int = 5

    def __init__(self):
        self.__switch_time_in_secs: int = 0
        self.__time_left_in_secs: int = 50
        self.__current_light: Light = Light.RED

    def __display(self, use_switch_time: bool = False):
        print('{:0>2}\t{} Light'.format(self.__switch_time_in_secs if use_switch_time else self.__time_left_in_secs,
                                        self.__current_light))
        sleep(1)

    def run(self):
        try:
            while True:
                if self.__current_light is Light.RED:
                    if self.__time_left_in_secs > 0:
                        self.__display()
                        self.__time_left_in_secs -= 1

                    else:
                        if self.__switch_time_in_secs:
                            self.__current_light = Light.YELLOW

                        else:
                            self.__display()

                elif self.__current_light is Light.YELLOW:
                    if self.__switch_time_in_secs > 0:
                        self.__display(True)
                        self.__switch_time_in_secs -= 1

                    else:
                        self.__current_light = Light.GREEN
                        self.__time_left_in_secs = 20

                elif self.__current_light is Light.GREEN:
                    if self.__time_left_in_secs > 0:
                        self.__display()
                        self.__time_left_in_secs -= 1

                    else:
                        self.__current_light = Light.RED
                        self.__time_left_in_secs = 50

        except KeyboardInterrupt:
            if self.__current_light is Light.RED:
                self.__switch_time_in_secs = self.DEFAULT_SWITCH_TIME_SECS
                self.run()

            else:
                self.run()


if __name__ == '__main__':
    tl = TrafficLight()
    tl.run()
