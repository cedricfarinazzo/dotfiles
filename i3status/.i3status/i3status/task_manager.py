from enum import Enum

class TaskType(Enum):
    INSERT = 0
    UPDATE = 1
    DELETE = 2

tasks_ = []

class Task:

    def __init__(self, task_type, index):
        self.task_type =  task_type
        self.index = index

    def process(self, data):
        return data

    def get_type(self):
        return self.task_type

    @staticmethod
    def register(t):
        if t is not None:
            tasks_.append(t)
        return t

    @staticmethod
    def update(data):
        for t in tasks_:
            data = t.process(data)
        return data

class TaskInsert(Task):

    def __init__(self, index, callback):
        super().__init__(TaskType.INSERT, index)
        self.callback = callback

    def process(self, data):
        data.insert(self.index, self.callback())
        return data

class TaskUpdate(Task):

    def __init__(self, index, callback):
        super().__init__(TaskType.UPDATE, index)
        self.callback = callback

    def process(self, data):
        self.callback(data[self.index])
        return data

class TaskDeleteIf(Task):

    def __init__(self, index, callback):
        super().__init__(TaskType.DELETE, index)
        self.callback = callback

    def process(self, data):
        if self.callback(data[self.index]):
            data.pop(self.index)
        return data


