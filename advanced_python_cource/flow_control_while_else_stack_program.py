class Program(object):
    @staticmethod
    def __is_comment(item: type) -> bool:
        return isinstance(item, str) and item.startswith('#')

    def execute(self, program: list):
        while program:
            item: type = program.pop()
            if not self.__is_comment(item):
                program.append(item)
                break

        else:
            print('Empty program.')
            return

        pending: list = []
        while program:
            item: type = program.pop()
            if callable(item):
                try:
                    result = item(*pending)
                except Exception as e:
                    print('Error: ', e)
                    break
                program.append(result)
                pending.clear()

            else:
                pending.append(item)

        else:
            print('Program successful.')
            print(f'Result: {pending}')

        print('Finished.')


if __name__ == '__main__':
    import operator

    init_vec = ('# some text', '# another text', 5, 2, operator.add, 3, operator.mul)
    reversed_vec = list(reversed(init_vec))

    p = Program()
    p.execute(reversed_vec)
