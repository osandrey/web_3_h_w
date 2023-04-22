import concurrent.futures
from multiprocessing import current_process, cpu_count
from time import time
import logging


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize_sinc(numbers: list) -> list:
    """
    Current function looking for factorial from every single number in provided list.
    :param numbers: list of numbers - type(int)
    :return: list
    """
    start_time = time()
    logger.debug(f'Start {start_time}')
    n_list = []

    for num in numbers:
        lst = []
        # print(type(num), num, sep='<-(-_-)->')
        for i in range(1, num + 1):
            if num % i == 0:
                lst.append(i)
        n_list.append(lst)
    logger.debug(f'Total time duration: {time() - start_time}')
    logger.debug(f'End {time()}')
    print(f'NNNNN___LIIISSSTTT: {n_list}')
    return n_list


def factorize_asinc(number: int) -> list:
    """
    Current function which takes numbers
    and returns lists of numbers that are part of the collected number without a remainder.
    :param number: number - type(int)
    :return: list
    """
    start_time = time()
    # logger.debug(f'Start {start_time}, Process: {current_process().name}')
    lst = []
    for i in range(1, number + 1):
        if number % i == 0:
            lst.append(i)
    logger.debug(f'Duration: {time() - start_time}, Process: {current_process().name}')
    print(lst)
    return lst


some_nums_list = [128, 255, 99999, 23422, 23422, 67865, 75433, 6444, 876890, 88755]


# a, b, c, d  = factorize_sinc(some_nums_list)
#
# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
#               380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
# print('Test is DONE !!!')

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(cpu_count()) as pool:
        logger.debug(f'Start in process: {cpu_count()}')
        result = pool.map(factorize_asinc, some_nums_list)
        print('%d is prime: %s', *result)
