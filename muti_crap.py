from multiprocessing.managers import BaseManager
from multiprocessing import Process, Lock

plane_lock = Lock()


class Plane(object):

    def __init__(self):
        self.count = 0

    def id(self):
        # plane_lock.acquire()
        self.count += 1
        # plane_lock.release()
        return {'hello': 55, 'bye': self.count}


class PlaneManager(BaseManager):
    pass


class HelloWorld(Process):

    def __init__(self, thread_id, plane, ip):
        Process.__init__(self)
        self.id = thread_id
        self.plane = plane

    def run(self):
        for i in range(0, 5000):
            print(self.id + " says Hello nr. " + str(i) + "; plane counter: " + str(self.plane.id()['bye']))
            i += 1


if __name__ == '__main__':
    PlaneManager.register('Plane', Plane)

    plane_manager = PlaneManager()
    plane_manager.start()

    ip = 'loser'

    closest_plane = plane_manager.Plane()
    hi1 = HelloWorld('1', closest_plane, ip)
    hi2 = HelloWorld('2', closest_plane, ip)
    hi3 = HelloWorld('3', closest_plane, ip)
    hi4 = HelloWorld('4', closest_plane, ip)

    hi1.start()
    hi2.start()
    hi3.start()
    hi4.start()

    hi1.join()
    hi2.join()
    hi3.join()
    hi4.join()
