import os
from pathlib import Path


class FileQueueByTime:
    def __init__(self):
        self.files = []
        self.index = -1

    def is_empty(self):
        return self.files

    def scan(self, path):
        self.files = sorted(Path(path).iterdir(), key=os.path.getmtime)

    def next(self):
        self.index += 1
        if len(self.files) > self.index:
            return self.files[self.index]
        else:
            return None

    def last(self):
        self.index -= 1
        if self.index >= 0:
            return self.files[self.index]
        else:
            return None