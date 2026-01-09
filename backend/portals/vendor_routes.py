"""Vendor portal routes: manage vendor products and related orders."""

from flask import jsonify, request

from models.database import db, User, UserRole, VendorProduct, Order, OrderStatus
from utils.auth import role_required, get_current_user


def register_vendor_routes(app):
    """Register all vendor-related routes on the given Flask app."""

    @app.route('/api/vendor/products', methods=['GET', 'POST'])
    @role_required(UserRole.VENDOR)
    def vendor_products():
        """Get or create vendor products"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.vendor_profile:
                return jsonify({'error': 'Vendor profile not found'}), 404

            if request.method == 'GET':
                products = (
                    VendorProduct.query.filter_by(vendor_id=user.vendor_profile.id)
                    .order_by(VendorProduct.created_at.desc())
                    .all()
                )

                return jsonify({
                    'success': True,
                    'products': [product.to_dict() for product in products],
                })

            data = request.json

            product = VendorProduct(
                vendor_id=user.vendor_profile.id,
                product_name=data['product_name'],
                category=data.get('category'),
                brand=data.get('brand'),
                quantity_available=float(data['quantity_available']),
                unit=data.get('unit', 'unit'),
                price_per_unit=float(data['price_per_unit']),
                description=data.get('description'),
                image_url=data.get('image_url'),
                specifications=data.get('specifications'),
            )

            db.session.add(product)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Product added',
                'product': product.to_dict(),
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/vendor/products/<int:product_id>', methods=['PUT', 'DELETE'])
    @role_required(UserRole.VENDOR)
    def manage_vendor_product(product_id):
        """Update or delete vendor product"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            product = VendorProduct.query.get(product_id)
            if not product or product.vendor_id != user.vendor_profile.id:
                return jsonify({'error': 'Product not found'}), 404

            if request.method == 'PUT':
                data = request.json

                if 'quantity_available' in data:
                    product.quantity_available = float(data['quantity_available'])
                if 'price_per_unit' in data:
                    product.price_per_unit = float(data['price_per_unit'])
                if 'is_available' in data:
                    product.is_available = bool(data['is_available'])
                if 'description' in data:
                    product.description = data['description']

                db.session.commit()
                return jsonify({'success': True, 'product': product.to_dict()})

            db.session.delete(product)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Product deleted'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/vendor/orders', methods=['GET'])
    @role_required(UserRole.VENDOR)
    def vendor_orders():
        """Get orders for vendor's products"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.vendor_profile:
                return jsonify({'error': 'Vendor profile not found'}), 404

            product_ids = [p.id for p in user.vendor_profile.products]

            orders = (
                Order.query
                .filter(Order.vendor_product_id.in_(product_ids))
                .order_by(Order.created_at.desc())
                .all()
            )

            results = []
            for order in orders:
                buyer = User.query.get(order.buyer_id)
                results.append({
                    'id': order.id,
                    'buyer_name': buyer.full_name if buyer else 'Unknown',
                    'buyer_email': buyer.email if buyer else None,
                    'product_name': (
                        order.vendor_product.product_name if order.vendor_product else None
                    ),
                    'quantity': order.quantity,
                    'total_price': order.total_price,
                    'status': order.status.value,
                    'delivery_date': order.delivery_date.isoformat()
                    if order.delivery_date
                    else None,
                    'created_at': order.created_at.isoformat(),
                })

            return jsonify({'success': True, 'orders': results})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/vendor/orders/<int:order_id>', methods=['PUT'])
    @role_required(UserRole.VENDOR)
    def vendor_update_order(order_id):
        """Update order status for orders containing this vendor's products."""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user or not user.vendor_profile:
                return jsonify({'error': 'Vendor profile not found'}), 404

            order = Order.query.get(order_id)
            if not order or not order.vendor_product_id:
                return jsonify({'error': 'Order not found'}), 404

            # Ensure the order belongs to this vendor
            product_ids = {p.id for p in user.vendor_profile.products}
            if order.vendor_product_id not in product_ids:
                return jsonify({'error': 'Not authorized to update this order'}), 403

            data = request.json or {}
            new_status = data.get('status')
            if not new_status:
                return jsonify({'error': 'Missing status'}), 400

            try:
                order.status = OrderStatus(new_status)
            except ValueError:
                allowed = [s.value for s in OrderStatus]
                return jsonify({'error': f'Invalid status. Allowed: {allowed}'}), 400

            db.session.commit()
            return jsonify({'success': True, 'message': 'Order updated', 'order': {
                'id': order.id,
                'status': order.status.value,
            }})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
