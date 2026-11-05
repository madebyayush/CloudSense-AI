import boto3
from datetime import datetime, timedelta, timezone

AWS_REGION = "ap-southeast-2"
INSTANCE_ID = "i-0d36180c2c766938d"

class CloudWatchMonitor:
    def __init__(self):
        self.client = boto3.client(
            "cloudwatch",
            region_name=AWS_REGION
        )

    def get_cpu_metrics(self):
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=3)

        response = self.client.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": INSTANCE_ID
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average"]
        )

        datapoints = sorted(
            response.get("Datapoints", []),
            key=lambda x: x["Timestamp"]
        )

        return [
            {
                "timestamp": p["Timestamp"].isoformat(),
                "cpu": round(p["Average"], 3)
            }
            for p in datapoints
        ]

monitor = CloudWatchMonitor()
