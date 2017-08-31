from random import choice

my_dict = {'подтверждать': 'confirm', 'замечать': 'spot', 'исходные данные': 'benchmark data',
           'подводить итог': 'conclude', 'ускорение': 'boost', 'сомневаться': 'doubt ', 'а не': 'rather than',
           'обещать': 'promise', 'пообещать': 'guarantee', 'выработать': 'deliver', 'взаимодействовать': 'interact',
           'отчетный период': 'report period', 'однородный': 'homogeneous', 'запись': 'record', 'извлечение': 'extract'}


class EngDict(object):
    def __init__(self):
        self.fully_successfully = True
        self.difficulty_level = 0
        self.attempts_per_answer = 3
        self.attempts_per_factor = 3
        self.square = 2

    def choice_word(self):

        if self.fully_successfully:
            try:
               print()
            except Exception:
                pass


    print(choice(list(my_dict)))
