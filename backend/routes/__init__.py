"""Routes package"""
from .auth_routes import register_auth_routes
from .error_handlers import register_error_handlers

__all__ = ['register_auth_routes', 'register_error_handlers']
