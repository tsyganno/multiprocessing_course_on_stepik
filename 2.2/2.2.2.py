"""
Напишите функцию print_process_info, которая выводит в консоль информацию о вызвавшем ее процессе и вызывает целевую функцию, переданную в качестве единственного аргумента.

Функция должна печать следующую информацию о процессе:
Процесс: <имя текущего процесса>, PID=<pid текущего процесса>, daemon=<признак демона текущего процесса(True|False)>
Родительский процесс: <имя родительского процесса>, PID=<pid родительского процесса>
Целевая задача процесса: <имя целевой задачи текущего процесса (func.__name__)>
а затем вызвать целевую функцию, переданную в качестве аргумента.

Например, если бы тест. система создала и запустила дочерний процесс с такой целевой функцией:

import multiprocessing
from typing import Callable


def task():
    print("Вызвана целевая задача...")


def print_process_info(func: Callable):
   pass  # допишите функцию


if __name__ == '__main__':
    pr = multiprocessing.Process(target=print_process_info, args=[task])
    pr.start()
    pr.join()
То Ваше решение должно вывести в консоль следующее:

Процесс: Process-1, PID=24740, daemon=False
Родительский процесс: MainProcess, PID=11924
Целевая задача процесса: task
Вызвана целевая задача...
Конечно, pid у Вас будут другими.

Определите функцию, а тестирующая система запустит ее дважды в разных дочерних процессах.
"""

import multiprocessing
from typing import Callable


# Ваше решение
def print_process_info(func: Callable):
    print(f'Процесс: {multiprocessing.current_process().name}, PID={multiprocessing.current_process().pid}, daemon={multiprocessing.current_process().daemon}\nРодительский процесс: {multiprocessing.parent_process().name}, PID={multiprocessing.parent_process().pid}\nЦелевая задача процесса: {func.__name__}')
    func()
