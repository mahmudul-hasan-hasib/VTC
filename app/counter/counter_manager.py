from app.counter.vehicle_data import VEHICLE_CLASSES


class CounterManager:

    def __init__(self):
        self.mode = "Incoming"
        self.history = []
        self.incoming = {name: 0 for name in VEHICLE_CLASSES}
        self.outgoing = {name: 0 for name in VEHICLE_CLASSES}

    def set_mode(self, mode):
        self.mode = mode

    def get_counts(self):
        if self.mode == "Incoming":
            return self.incoming
        return self.outgoing

    def increment(self, vehicle):
        counts = self.get_counts()
        counts[vehicle] += 1
        self.history.append((self.mode, vehicle))

    def undo(self):
        if not self.history:
            return
        mode, vehicle = self.history.pop()
        if mode == "Incoming":
            counts = self.incoming
        else:
            counts = self.outgoing
        if counts[vehicle] > 0:
            counts[vehicle] -= 1

    def decrement(self, vehicle):
        counts = self.get_counts()
        if counts[vehicle] > 0:
            counts[vehicle] -= 1

    def total(self):
        return sum(self.get_counts().values())

    def reset_current(self):
        counts = self.get_counts()
        for k in counts:
            counts[k] = 0
        self.history = [(m, v) for m, v in self.history if m != self.mode]

    def reset(self):
        for k in self.incoming:
            self.incoming[k] = 0
        for k in self.outgoing:
            self.outgoing[k] = 0
        self.history.clear()
