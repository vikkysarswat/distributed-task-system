"""Prometheus metrics configuration."""

from prometheus_client import Counter, Histogram, Gauge, Info

# Task metrics
task_counter = Counter(
    'tasks_total',
    'Total number of tasks',
    ['task_type', 'priority', 'status']
)

task_duration_histogram = Histogram(
    'task_duration_seconds',
    'Task execution duration in seconds',
    ['task_type'],
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 300.0, 600.0, float('inf'))
)

task_queue_size = Gauge(
    'task_queue_size',
    'Number of tasks in queue',
    ['queue_name']
)

active_workers = Gauge(
    'active_workers',
    'Number of active workers',
    ['worker_type']
)

# HTTP metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Database metrics
db_connections = Gauge(
    'db_connections',
    'Number of database connections',
    ['state']  # active, idle
)

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['operation']
)

# Cache metrics
cache_operations = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['operation', 'result']  # hit, miss, error
)

# System info
system_info = Info(
    'system_info',
    'System information'
)


def init_metrics():
    """Initialize metrics with system information."""
    system_info.info({
        'version': '1.0.0',
        'python_version': '3.11',
        'environment': 'production'
    })