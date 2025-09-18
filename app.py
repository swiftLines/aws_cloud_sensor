from flask import Flask, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import os, time


app = Flask(__name__)
start_time = time.time()

REQUESTS = Counter("cloud_sensor_requests_total", "Total HTTP requests", ["endpoint"])
HEALTH_OK = Gauge("cloud_sensor_health_ok", "1 if healthy else 0")
READY_OK = Gauge("cloud_sensor_ready_ok", "1 if ready else 0")


@app.route("/healthz")
def healthz():
    REQUESTS.labels("/healthz").inc()
    HEALTH_OK.set(1)
    return jsonify(status="ok", uptime_sec=int(time.time() - start_time))


@app.route("/readyz")
def readyz():
    REQUESTS.labels("/readyz").inc()
    # Startup delay to simulate readiness gates
    delay = int(os.getenv("READY_DELAY_SEC", "0"))
    ready = (time.time() - start_time) >= delay
    READY_OK.set(1 if ready else 0)
    return (jsonify(ready=ready), 200 if ready else 503)


@app.route("/metrics")
def metrics():
    REQUESTS.labels("/metrics").inc()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
