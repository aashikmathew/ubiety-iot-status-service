from prometheus_client import Counter, Gauge

# Prometheus metrics
heartbeat_counter = Counter("heartbeat_count", "Number of heartbeats received")
at_risk_gauge = Gauge("at_risk_devices", "Number of at-risk devices")
online_gauge = Gauge("online_devices", "Number of online devices")
avg_battery_gauge = Gauge("average_battery", "Average battery level of devices") 