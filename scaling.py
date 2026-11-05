class ScalingEngine:
    """
    Predictive policy with conservative bounds.
    Increases capacity if predicted CPU is high; reduces only at low demand.
    """
    def __init__(self, min_instances=1, max_instances=6):
        self.min_instances = min_instances
        self.max_instances = max_instances

    def decide(self, predicted_cpu, current_instances):
        if predicted_cpu >= 75 and current_instances < self.max_instances:
            new_count = min(self.max_instances, current_instances + 1)
            return {
                "action": "SCALE UP",
                "recommended_instances": new_count,
                "reason": f"Predicted CPU is {predicted_cpu:.1f}%, above the 75% scale-up threshold."
            }
        if predicted_cpu <= 30 and current_instances > self.min_instances:
            new_count = max(self.min_instances, current_instances - 1)
            return {
                "action": "SCALE DOWN",
                "recommended_instances": new_count,
                "reason": f"Predicted CPU is {predicted_cpu:.1f}%, below the 30% scale-down threshold."
            }
        return {
            "action": "MAINTAIN",
            "recommended_instances": current_instances,
            "reason": f"Predicted CPU is {predicted_cpu:.1f}%; capacity remains within the target operating range."
        }
