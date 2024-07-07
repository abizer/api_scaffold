import time
from typing import List


class timer:
    def __init__(self):
        self.started = 0
        self.stopped = 0
        self.laps = []

    def start(self) -> None:
        self.started = time.perf_counter_ns()
        self.laps.append(self.started)

    def elapsed(self) -> int:
        return (time.perf_counter_ns() - self.started) / 1_000_000

    def lap(self) -> int:
        self.laps.append(time.perf_counter_ns())

    def reset(self) -> int:
        self.started = time.perf_counter_ns()
        self.laps = []

    def stop(self) -> int:
        self.stopped = time.perf_counter_ns()
        self.laps.append(self.stopped)

    def deltas(self) -> List[float]:
        return [
            "{:.3f}ms".format(round((self.laps[i] - self.laps[i - 1]) / 1_000_000, 3))
            for i in range(1, len(self.laps))
        ]

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def __str__(self):
        return f"{(self.stopped-self.started)/1_000_000:.3f}ms {self.deltas()}"
