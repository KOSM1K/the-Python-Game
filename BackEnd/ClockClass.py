import time


class Clock:
    def __init__(self, Herz: float = 1):
        self.lastTick = time.time()
        self.delay = 1 / Herz

    def changeFrequency(self, Herz: float = 1):
        self.delay = 1 / Herz

    def waitNewTick(self, highPrecision: bool = True, forcedTick: bool = False):
        overlay = (time.time() - self.lastTick) / self.delay
        if highPrecision:
            while time.time() - self.lastTick < self.delay:
                pass
        else:
            time.sleep(max(0.0, self.delay - time.time() - self.lastTick))

        if forcedTick:
            self.lastTick += self.delay
        else:
            self.lastTick = time.time()

        return overlay
