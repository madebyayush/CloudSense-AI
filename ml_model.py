import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

class ResourcePredictor:
    """
    Trains a small Random Forest on reproducible synthetic workload samples.
    The target is next-interval CPU utilization (0-100%).
    """
    def __init__(self):
        rng = np.random.default_rng(42)
        n = 2500
        requests = rng.integers(20, 3001, n)
        cpu_now = rng.uniform(5, 99, n)
        memory = np.clip(cpu_now * 0.72 + rng.normal(2, 8, n), 5, 99)
        cpu_prev = np.clip(cpu_now + rng.normal(0, 12, n), 0, 100)
        # Synthetic target relationship: workload intensity + trend + noise.
        target = np.clip(
            0.58 * cpu_now + 0.25 * cpu_prev +
            0.006 * requests + 0.08 * memory +
            rng.normal(0, 5, n), 0, 100
        )
        X = np.column_stack([cpu_now, memory, requests, cpu_prev])
        X_train, X_test, y_train, y_test = train_test_split(
            X, target, test_size=0.2, random_state=42
        )
        self.model = RandomForestRegressor(
            n_estimators=100, max_depth=12, min_samples_leaf=2,
            random_state=42, n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        self.metrics = {
            "algorithm": "Random Forest Regression",
            "training_samples": int(len(X_train)),
            "testing_samples": int(len(X_test)),
            "mae": round(float(mean_absolute_error(y_test, predictions)), 3),
            "rmse": round(float(np.sqrt(mean_squared_error(y_test, predictions))), 3),
            "features": ["current_cpu", "memory", "requests_per_minute", "previous_cpu"],
            "data_note": "Synthetic demonstration dataset; replace with measured workload data for research claims."
        }

    def predict(self, metrics):
        row = [[
            metrics["cpu"], metrics["memory"],
            metrics["requests_per_minute"], metrics["cpu_previous"]
        ]]
        return float(self.model.predict(row)[0])
