"""
Напишите класс специализированного процесса - обработчика CSV файлов CSVHandler, который:

Наследуется от Process.
Имеет дополнительные атрибуты:
files - коллекция (list, tuple) с именами файлов для обработки;
worker - функция обработки (вызываемый объект). Единственный аргумент функции принимает название файла;
timeout - значение таймаута (int, float, значение по умолчанию 1 секунда,).
При необходимости можно создавать дополнительные атрибуты.
Во время запуска создает отдельный дочерний процесс обработки для каждого файла.
После создания и запуска всех дочерних процессов обработки ожидает необходимый таймаут и проверяет статус каждого процесса обработки. Если процесс все еще занимается обработкой, считаем, что он "завис", его нужно принудительно завершить и очистить его ресурсы, также выполняется вывод в консоль:
<file> processing timeout exceeded
где <file> - имя файла обработки, на котором "завис" процесс.
В решении используйте контекст.

Создание и запуск экземпляра CSVHandler проверяет тестирующая система. Функция обработки, значение таймаута и коллекция файлов для обработки - все это реализовано в тестирующей системе. Вам нужно только написать класс.
Тестирующая система создаст экземпляр класса, установит таймаут и запустит:

if __name__ == '__main__':
    filenames = ['file_1.csv', 'file_2.csv', 'file_3.csv', ....]  # список файлов CSV для обработки
    csv_worker = CSVHandler(filenames, worker)
    csv_worker.timeout = ...
    csv_worker.start()
"""

import multiprocessing as mp
import time


class CSVHandler(mp.Process):
    def __init__(self, files: list[str] | tuple[str] = None, worker: callable = None, timeout: int = 1):
        super().__init__()
        self.files, self.worker, self.timeout, self.processes = files, worker, timeout, []

    def run(self):
        for file in self.files:
            p = mp.Process(target=self.worker, args=(file,))
            p.start()
            self.processes.append((file, p))

        time.sleep(self.timeout)

        for file, p in self.processes:
            if p.is_alive():
                print(f"{file} processing timeout exceeded")
                p.terminate()
                p.join()
                p.close()
