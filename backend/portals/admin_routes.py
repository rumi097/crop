"""Admin portal routes: user management and analytics."""

from flask import jsonify, request

from models.database import User, UserRole, Order, CropListing, VendorProduct, db
from utils.auth import role_required


def register_admin_routes(app):
    """Register all admin-related routes on the given Flask app."""

    @app.route('/api/admin/users', methods=['GET'])
    @role_required(UserRole.ADMIN)
    def admin_get_users():
        """Get all users for admin"""
        try:
            role_filter = request.args.get('role')
            users = (
                User.query.all()
                if not role_filter
                else User.query.filter_by(role=UserRole(role_filter)).all()
            )

            results = [user.to_dict() for user in users]
            return jsonify({'success': True, 'users': results})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/admin/verify-user/<int:user_id>', methods=['POST'])
    @role_required(UserRole.ADMIN)
    def admin_verify_user(user_id):
        """Verify a user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user.is_verified = True
            db.session.commit()

            return jsonify({'success': True, 'message': 'User verified'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/admin/analytics', methods=['GET'])
    @role_required(UserRole.ADMIN)
    def admin_analytics():
        """Get platform analytics"""
        try:
            total_users = User.query.count()
            total_farmers = User.query.filter_by(role=UserRole.FARMER).count()
            total_buyers = User.query.filter_by(role=UserRole.BUYER).count()
            total_vendors = User.query.filter_by(role=UserRole.VENDOR).count()
            total_labor = User.query.filter_by(role=UserRole.LABOR).count()
            total_orders = Order.query.count()
            total_crops = CropListing.query.count()
            total_products = VendorProduct.query.count()

            return jsonify({
                'success': True,
                'analytics': {
                    'total_users': total_users,
                    'farmers': total_farmers,
                    'buyers': total_buyers,
                    'vendors': total_vendors,
                    'labor': total_labor,
                    'total_orders': total_orders,
                    'total_crops': total_crops,
                    'total_products': total_products,
                },
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500
