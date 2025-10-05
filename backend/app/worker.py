import logging
import os
import sys
from rq import Worker, Queue, Connection
import redis

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Run RQ worker"""
    # Connect to Redis
    redis_conn = redis.from_url(settings.REDIS_URL)
    
    # Create queues
    queues = [
        Queue('ingest', connection=redis_conn),
        Queue('refresh', connection=redis_conn),
        Queue('notify', connection=redis_conn),
        Queue('default', connection=redis_conn),
    ]
    
    # Start worker
    logger.info("Starting RQ worker...")
    worker = Worker(queues, connection=redis_conn)
    worker.work()

if __name__ == '__main__':
    main()