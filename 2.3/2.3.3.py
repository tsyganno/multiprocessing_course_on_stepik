"""
Напишите класс для параллельной обработки задач ParallelExecuter, который:

Имеет атрибуты:
log - список со статусом исполнения каждой задачи. Длина списка равна количеству объектов - задач;
timeout - значение таймаута (int, float, значение по умолчанию - None).
При необходимости можно создавать дополнительные атрибуты.
Конструктор класса должен принимать:
- ​​​​​​список или кортеж вызываемых объектов - задач,
- список или кортеж из аргументов для каждой задачи (каждая задача может иметь несколько аргументов!). Для решения достаточно предусмотреть только передачу позиционных аргументов,
- необязательный аргумент - timeout, уставка максимального времени ожидания завершения всех задач. Если аргумент не задан - время ожидания не ограничено. Если аргумент задан (int, количество секунд), то выполняется контроль длительности выполнения задач. Если за отведенное время задачи не успевают завершиться, процесс, который выполняет такую длительную задачу, должен быть завершен принудительно
Во время запуска методом execute() создает и запускает отдельные процессы для выполнения каждой из задач. Метод является блокирующим, т.к. после создания и запуска всех дочерних процессов обработки ожидает необходимый таймаут и проверяет статус каждого процесса выполнения задачи. Если процесс все еще выполняется, считаем, что он "завис", его нужно принудительно завершить и очистить его ресурсы, в лог для такой задачи в качестве значения устанавливается текст:
<task> processing timeout exceeded
где <task> - имя задачи (task.name), на котором "завис" процесс.
Если задача завершилась вовремя, в список лога добавляется:
<task> completed successfully
Порядок значений в логе должен соответствовать порядку переданных в конструктор задач на исполнение.
(Имя задачи можно получить вызвав дандер метод __name__ (task.__name__))
В решении используйте контекст. Не используйте функцию sleep.

Создание и запуск экземпляра ParallelExecuter проверяет тестирующая система. Тестирующая система вызовет метод execute() и проверит время решения.
"""


import multiprocessing as mp
import time


class ParallelExecuter:
    def __init__(self, tasks, args, timeout=None):
        self.tasks = tasks
        self.args = args
        self.timeout = timeout
        self.log = [None] * len(tasks)

    def execute(self):
        processes = []
        start_time = time.time()

        for task, task_args in zip(self.tasks, self.args):
            p = mp.Process(target=task, args=task_args)
            p.start()
            processes.append((task.__name__, p))

        for i, (name, p) in enumerate(processes):
            if self.timeout is not None:
                elapsed = time.time() - start_time
                remaining = self.timeout - elapsed
                if remaining <= 0:
                    # Времени уже не осталось, завершить и записать в лог
                    if p.is_alive():
                        p.terminate()
                        p.join()
                        self.log.append(f"{name} processing timeout exceeded")
                        self.log.remove(None)
                        continue

                p.join(timeout=remaining)
            else:
                p.join()

            if p.is_alive():
                p.terminate()
                p.join()
                self.log.append(f"{name} processing timeout exceeded")
            else:
                self.log.append(f"{name} completed successfully")
            self.log.remove(None)
