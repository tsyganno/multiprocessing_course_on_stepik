import multiprocessing


def main():
    for source in sources:
        multiprocessing.Process(target=handler, args=(source, )).start()


if __name__ == '__main__':
    main()
