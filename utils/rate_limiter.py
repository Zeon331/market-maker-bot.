import time
import asyncio

class RateLimiter:
    def __init__(self, max_req, period):
        self.max_req = max_req
        self.period = period
        self.timestamps = []

    async def wait(self):
        while True:
            now = time.time()
            self.timestamps = [t for t in self.timestamps if now - t < self.period]
            
            if len(self.timestamps) < self.max_req:
                self.timestamps.append(now)
                return
            
            sleep_time = self.period - (now - self.timestamps[0])
            await asyncio.sleep(sleep_time)