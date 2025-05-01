import multiprocessing


def main():
    pr = multiprocessing.Process(target=task, daemon=False)
    pr.start()


if __name__ == '__main__':
    main()
