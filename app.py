from flask import Flask, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import os, time


app = Flask(__name__)
start_time = time.time()

REQUESTS = Counter("cloud_sensor_requests_total", "Total HTTP requests", ["endpoint"])