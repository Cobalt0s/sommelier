# custom class wrapping a list in order to make it thread safe
from threading import Lock


class ThreadSafeList(object):
    # constructor
    def __init__(self):
        # initialize the list
        self._list = list()
        # initialize the lock
        self._lock = Lock()

    # add a value to the list
    def append(self, value):
        # acquire the lock
        with self._lock:
            # append the value
            self._list.append(value)

    # remove and return the last value from the list
    def pop(self):
        # acquire the lock
        with self._lock:
            # pop a value from the list
            if len(self._list) == 0:
                return None
            return self._list.pop()

    # read a value from the list at an index
    def get(self, index):
        # acquire the lock
        with self._lock:
            # read a value at the index
            return self._list[index]

    # return the number of items in the list
    def length(self):
        # acquire the lock
        with self._lock:
            return len(self._list)
