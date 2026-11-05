import random
from datetime import datetime

class WorkloadSimulator:
    MODES = ("low", "normal", "spike")

    def __init__(self):
        self.tick = 0
        self.cpu_history = [25.0, 28.0, 30.0]

    def reset(self):
        self.tick = 0
        self.cpu_history = [25.0, 28.0, 30.0]

    def next_metrics(self, mode="normal"):
        self.tick += 1
        ranges = {
            "low": (10, 30, 80, 250),
            "normal": (30, 65, 250, 900),
            "spike": (75, 98, 1000, 3000)
        }
        cmin, cmax, rmin, rmax = ranges[mode]
        cpu = random.uniform(cmin, cmax)
        requests = random.randint(rmin, rmax)
        memory = min(95, max(10, cpu * 0.72 + random.uniform(-8, 12)))
        self.cpu_history.append(cpu)
        self.cpu_history = self.cpu_history[-3:]
        return {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "cpu": round(cpu, 2),
            "memory": round(memory, 2),
            "requests_per_minute": requests,
            "cpu_previous": round(self.cpu_history[-2], 2) if len(self.cpu_history) > 1 else round(cpu, 2),
            "workload_mode": mode
        }
