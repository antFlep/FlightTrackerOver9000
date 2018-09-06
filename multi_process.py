from multiprocessing import Process, Manager, Lock, Array


def f(d, lock):
    lock.aquire()
    d[1] = d[1]-1
    lock.release()

def f_array(array, lock):
    lock.acquire()
    # modify array here
    array[0] = array[0]+1
    lock.release()


if __name__ == '__main__':
    manager = Manager()
    size = 100
    arr = Array('i', size)  # c type array
    print(arr)
    lock = Lock()
    p = Process(target=f_array, args=(arr, lock,))
    q = Process(target=f_array, args=(arr, lock,))
    p.start()
    q.start()
    q.join()
    p.join()

    print(arr[0])


