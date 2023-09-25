import argparse
import itertools
import logging

from functools import wraps
from time import time

logging.basicConfig(level=logging.INFO)

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logging.debug('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        with open("x", "w+") as t:
            t.write('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        return result
    return wrap


def parse_arguments():
    """Получаем аргументы"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--to', type=str, help='Right')
    parser.add_argument('--from', type=str, help='Left')
    args = parser.parse_args()

    return args


def check_arguments_ok(from_arg: str, to_arg: str) -> bool:
    """"Проверка аргументов, допустимы только символы из [a-z] в нижнем регистре"""

    from_ok = from_arg.isascii() and from_arg.isalpha() and from_arg.islower()
    to_ok = to_arg.isascii() and to_arg.isalpha() and to_arg.islower()
    len_ok = len(to_arg) >= len(from_arg)

    return from_ok and to_ok and len_ok

def check_acceptance(variable: str, from_s: str, to: str) -> bool:
    """
    Вариант подходит если его длина равна длине строки from_s и он лексикографически больше или равен ей;
    ИЛИ если длина варианта равна длине строки to и он лексикографически меньше или равен ей
    Если длина варианта внутри этого диапазона, он подходит всегда

    Внимание: если длины строк from и to равны, проверяем выбор варианта отдельно
    """

    # отдельный кейс: если у from и to длины равны
    sm_length = len(variable) == len(from_s) and len(variable) == len(to)
    sm_length_match = from_s <= variable <= to

    # если не равны
    left_ok = len(variable) == len(from_s) and variable >= from_s
    right_ok = len(variable) == len(to) and variable <= to

    if not sm_length:
        return left_ok or right_ok
    else:
        return sm_length_match

@timing
def get_combinations(from_str: str, to_str: str) -> list:
    """
    Генерируем все возможные сочетания букв алфавита, начиная с минимальной длины
    и добавляем только те, которые подходят
    """
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    result = []
    if check_arguments_ok(from_str, to_str):
        for i in range(len(from_str), len(to_str)+1):
            result.append(["".join(p) for p in itertools.product(alphabet, repeat=i)
                           if check_acceptance("".join(p), from_str, to_str)])
        return result
    else:
        logging.error("Illegal arguments")
        raise ValueError(f"Only [a-z] lowercase, given: {from_str} and {to_str}")


def main():
    args = parse_arguments()
    from_letters = args.__getattribute__("from")  # args.from - совпадение с кейвордом
    to_letters = args.to

    if from_letters is None or to_letters is None:
        logging.error("One parameter is missed")
    else:
        logging.info(f"Print all combinations from {from_letters} to {to_letters}")
        x = get_combinations(from_letters, to_letters)
        flat_list = [item for sublist in x for item in sublist]
        print("\n".join(flat_list))
        logging.info(x)


if __name__ == '__main__':
    main()
