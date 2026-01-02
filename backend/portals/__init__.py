"""Portal-specific route registration helpers.

Each portal module exposes a ``register_*_routes(app)`` function
that attaches its endpoints to the main Flask application. This
keeps ``app.py`` focused on configuration and cross-cutting
concerns while portal logic lives in dedicated modules.
"""

from .farmer_routes import register_farmer_routes
from .buyer_routes import register_buyer_routes
from .vendor_routes import register_vendor_routes
from .labor_routes import register_labor_routes
from .admin_routes import register_admin_routes

__all__ = [
	"register_farmer_routes",
	"register_buyer_routes",
	"register_vendor_routes",
	"register_labor_routes",
	"register_admin_routes",
]
