from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response
import time

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
active_connections = Gauge('active_connections', 'Active connections')
database_connections = Gauge('database_connections_active', 'Active database connections')
redis_connections = Gauge('redis_connections_active', 'Active Redis connections')

def setup_metrics(app: FastAPI):
    """Setup Prometheus metrics endpoint"""
    
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        return Response(
            generate_latest(),
            media_type="text/plain"
        )