"""Utility decorators for performance monitoring and logging."""

import asyncio
import functools
import time
from typing import Any, Callable, TypeVar

import structlog
from prometheus_client import Histogram

# Create logger
logger = structlog.get_logger(__name__)

# Performance metrics
function_duration = Histogram(
    'function_duration_seconds',
    'Function execution duration',
    ['function_name', 'module']
)

F = TypeVar('F', bound=Callable[..., Any])


def measure_performance(func: F) -> F:
    """Decorator to measure function performance."""
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            function_duration.labels(
                function_name=func.__name__,
                module=func.__module__
            ).observe(duration)
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            function_duration.labels(
                function_name=func.__name__,
                module=func.__module__
            ).observe(duration)
    
    # Return appropriate wrapper based on function type
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def log_execution(func: F) -> F:
    """Decorator to log function execution."""
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger.info(
            "Function execution started",
            function=func.__name__,
            module=func.__module__
        )
        
        try:
            result = await func(*args, **kwargs)
            logger.info(
                "Function execution completed",
                function=func.__name__,
                module=func.__module__
            )
            return result
        except Exception as e:
            logger.error(
                "Function execution failed",
                function=func.__name__,
                module=func.__module__,
                error=str(e),
                exc_info=True
            )
            raise
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger.info(
            "Function execution started",
            function=func.__name__,
            module=func.__module__
        )
        
        try:
            result = func(*args, **kwargs)
            logger.info(
                "Function execution completed",
                function=func.__name__,
                module=func.__module__
            )
            return result
        except Exception as e:
            logger.error(
                "Function execution failed",
                function=func.__name__,
                module=func.__module__,
                error=str(e),
                exc_info=True
            )
            raise
    
    # Return appropriate wrapper based on function type
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper