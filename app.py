from flask import Flask, jsonify, render_template, request
from simulator import WorkloadSimulator
from ml_model import ResourcePredictor
from scaling import ScalingEngine

app = Flask(__name__)
simulator = WorkloadSimulator()
predictor = ResourcePredictor()
scaler = ScalingEngine()

state = {
    "instances": 2,
    "history": [],
    "last": None,
    "mode": "normal"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({"state": state, "model": predictor.metrics})

@app.route("/api/step", methods=["POST"])
def step():
    payload = request.get_json(silent=True) or {}
    mode = payload.get("mode", state["mode"])
    if mode not in simulator.MODES:
        return jsonify({"error": "Unknown workload mode"}), 400

    state["mode"] = mode
    metrics = simulator.next_metrics(mode)
    predicted_cpu = predictor.predict(metrics)
    decision = scaler.decide(predicted_cpu, state["instances"])
    old_instances = state["instances"]
    state["instances"] = decision["recommended_instances"]

    # Transparent illustrative cost model, not an AWS bill.
    hourly_rate = 0.01
    estimated_hourly_cost = state["instances"] * hourly_rate
    baseline_cost = 4 * hourly_rate

    result = {
        **metrics,
        "predicted_cpu": round(predicted_cpu, 2),
        "previous_instances": old_instances,
        "instances": state["instances"],
        "action": decision["action"],
        "reason": decision["reason"],
        "estimated_hourly_cost": round(estimated_hourly_cost, 4),
        "baseline_hourly_cost": round(baseline_cost, 4),
        "estimated_savings_percent": round(max(0, (baseline_cost-estimated_hourly_cost)/baseline_cost*100), 1)
    }
    state["last"] = result
    state["history"].append(result)
    state["history"] = state["history"][-40:]
    return jsonify(result)

@app.route("/api/reset", methods=["POST"])
def reset():
    simulator.reset()
    state.update({"instances": 2, "history": [], "last": None, "mode": "normal"})
    return jsonify({"ok": True})

@app.route("/api/model")
def model_info():
    return jsonify(predictor.metrics)
@app.route("/api/cloudwatch")
def cloudwatch_data():
    try:
        from cloudwatch_monitor import monitor

        metrics = monitor.get_cpu_metrics()

        return jsonify({
            "status": "success",
            "source": "Amazon CloudWatch",
            "instance_id": "i-0d36180c2c766938d",
            "region": "ap-southeast-2",
            "metrics": metrics,
            "latest_cpu": metrics[-1]["cpu"] if metrics else None
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
