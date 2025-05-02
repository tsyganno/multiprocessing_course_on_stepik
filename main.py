import multiprocessing as mp
from time import sleep
import os


def task(n: int):
    sleep(n)


def main():
    prs = [mp.Process(target=task, args=(i, )) for i in range(4)]
    for pr in prs:
        pr.start()
    sleep(0.5)
    for pr in mp.active_children():
        print(f"{pr.name=}, {pr.pid=}")


if __name__ == "__main__":
    main()
    print(mp.current_process().pid)

