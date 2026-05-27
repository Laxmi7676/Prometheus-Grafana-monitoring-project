from flask import Flask
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import random
import time

app = Flask(__name__)

# metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint']
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

@app.route('/')
def home():
    start = time.time()
    ACTIVE_USERS.set(random.randint(10, 100))
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
    return 'Hello! App is running.'

@app.route('/error')
def error():
    REQUEST_COUNT.labels(method='GET', endpoint='/error', status='500').inc()
    return 'Something went wrong!', 500

@app.route('/slow')
def slow():
    start = time.time()
    time.sleep(random.uniform(0.5, 3.0))
    REQUEST_COUNT.labels(method='GET', endpoint='/slow', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/slow').observe(time.time() - start)
    return 'Slow response!'

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
