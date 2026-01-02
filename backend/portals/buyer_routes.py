"""Buyer portal routes: marketplace browsing and orders."""

from datetime import datetime

from flask import jsonify, request

from models.database import db, User, CropListing, VendorProduct, Order
from utils.auth import login_required, get_current_user


def register_buyer_routes(app):
    """Register all buyer-related routes on the given Flask app."""

    @app.route('/api/buyer/marketplace', methods=['GET'])
    @login_required
    def buyer_marketplace():
        """Browse marketplace for buyers"""
        try:
            category = request.args.get('category')
            search = request.args.get('search', '')

            # Get crop listings
            crop_query = CropListing.query.filter_by(is_available=True)
            if category:
                crop_query = crop_query.filter_by(category=category)
            if search:
                crop_query = crop_query.filter(CropListing.crop_name.ilike(f'%{search}%'))

            crops = crop_query.all()

            # Get vendor products
            product_query = VendorProduct.query.filter_by(is_available=True)
            if category:
                product_query = product_query.filter_by(category=category)
            if search:
                product_query = product_query.filter(VendorProduct.product_name.ilike(f'%{search}%'))

            products = product_query.all()

            return jsonify({
                'success': True,
                'crops': [crop.to_dict() for crop in crops],
                'products': [product.to_dict() for product in products]
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/buyer/orders', methods=['GET', 'POST'])
    @login_required
    def buyer_orders():
        """Get or create orders"""
        try:
            current_user = get_current_user()

            if request.method == 'GET':
                orders = (
                    Order.query
                    .filter_by(buyer_id=current_user['user_id'])
                    .order_by(Order.created_at.desc())
                    .all()
                )

                print(f"DEBUG: Found {len(orders)} orders for user {current_user['user_id']}")

                results = []
                for order in orders:
                    order_dict = {
                        'id': order.id,
                        'order_type': order.order_type,
                        'quantity': order.quantity,
                        'unit_price': order.unit_price,
                        'total_price': order.total_price,
                        'status': order.status.value,
                        'is_contract_farming': order.is_contract_farming,
                        'delivery_date': order.delivery_date.isoformat() if order.delivery_date else None,
                        'delivery_address': order.delivery_address,
                        'created_at': order.created_at.isoformat(),
                    }

                    try:
                        if order.order_type == 'crop' and order.crop_listing:
                            order_dict['product_name'] = order.crop_listing.crop_name
                            farmer_profile = order.crop_listing.farmer
                            if farmer_profile:
                                farmer_user = User.query.get(farmer_profile.user_id)
                                order_dict['seller_name'] = (
                                    farmer_user.full_name if farmer_user else 'Unknown Farmer'
                                )
                            else:
                                order_dict['seller_name'] = 'Unknown Farmer'
                        elif order.order_type == 'vendor_product' and order.vendor_product:
                            order_dict['product_name'] = order.vendor_product.product_name
                            vendor_profile = order.vendor_product.vendor
                            if vendor_profile:
                                vendor_user = User.query.get(vendor_profile.user_id)
                                order_dict['seller_name'] = (
                                    vendor_user.full_name if vendor_user else 'Unknown Vendor'
                                )
                            else:
                                order_dict['seller_name'] = 'Unknown Vendor'
                    except Exception as e:  # noqa: F841
                        print(f"DEBUG: Error loading order {order.id} details: {e}")
                        order_dict['product_name'] = 'Unknown Product'
                        order_dict['seller_name'] = 'Unknown Seller'

                    print(f"DEBUG: Order {order.id} - {order_dict.get('product_name', 'N/A')}")
                    results.append(order_dict)

                print(f"DEBUG: Returning {len(results)} orders")
                return jsonify({'success': True, 'orders': results})

            # POST: create order(s)
            data = request.json or {}

            # Support cart-based payload from frontend as well as legacy single-item payload
            if 'items' in data:
                if not isinstance(data['items'], list) or not data['items']:
                    return jsonify({'error': 'Items list is required'}), 400

                created_orders = []

                for item in data['items']:
                    item_type = item.get('type')
                    item_id = item.get('id')
                    quantity = float(item.get('quantity', 0))
                    if not item_type or not item_id or quantity <= 0:
                        return jsonify({'error': 'Invalid item in cart'}), 400

                    if item_type == 'crop':
                        crop = CropListing.query.get(item_id)
                        if not crop:
                            return jsonify({'error': 'Crop listing not found'}), 404
                        if crop.quantity < quantity:
                            return jsonify({'error': 'Insufficient quantity available for crop'}), 400
                        unit_price = float(crop.price_per_unit)
                        crop.quantity -= quantity
                        order_type = 'crop'
                        crop_listing_id = crop.id
                        vendor_product_id = None
                    else:
                        product = VendorProduct.query.get(item_id)
                        if not product:
                            return jsonify({'error': 'Vendor product not found'}), 404
                        if product.quantity_available < quantity:
                            return jsonify({'error': 'Insufficient quantity available for product'}), 400
                        unit_price = float(product.price_per_unit)
                        product.quantity_available -= quantity
                        order_type = 'vendor_product'
                        crop_listing_id = None
                        vendor_product_id = product.id

                    total_price = unit_price * quantity

                    order = Order(
                        buyer_id=current_user['user_id'],
                        order_type=order_type,
                        crop_listing_id=crop_listing_id,
                        vendor_product_id=vendor_product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        is_contract_farming=data.get('is_contract_farming', False),
                        delivery_date=None,
                        delivery_address=data.get('delivery_address'),
                        notes=data.get('notes'),
                    )
                    db.session.add(order)
                    created_orders.append(order)

                db.session.commit()

                return jsonify({
                    'success': True,
                    'message': 'Order(s) placed successfully',
                    'order_ids': [o.id for o in created_orders],
                }), 201

            # Legacy single-item payload (used by scripts/tests)
            if not all(k in data for k in ['order_type', 'quantity', 'unit_price']):
                return jsonify({'error': 'Missing required order fields'}), 400

            total_price = float(data['quantity']) * float(data['unit_price'])
            order_quantity = float(data['quantity'])

            # Check and update product quantities
            if data['order_type'] == 'crop':
                crop = CropListing.query.get(data.get('crop_listing_id'))
                if crop:
                    if crop.quantity < order_quantity:
                        return jsonify({'error': 'Insufficient quantity available'}), 400
                    crop.quantity -= order_quantity
            elif data['order_type'] == 'vendor_product':
                product = VendorProduct.query.get(data.get('vendor_product_id'))
                if product:
                    if product.quantity_available < order_quantity:
                        return jsonify({'error': 'Insufficient quantity available'}), 400
                    product.quantity_available -= order_quantity

            order = Order(
                buyer_id=current_user['user_id'],
                order_type=data['order_type'],
                crop_listing_id=data.get('crop_listing_id'),
                vendor_product_id=data.get('vendor_product_id'),
                quantity=order_quantity,
                unit_price=float(data['unit_price']),
                total_price=total_price,
                is_contract_farming=data.get('is_contract_farming', False),
                delivery_date=datetime.strptime(data['delivery_date'], '%Y-%m-%d').date()
                if data.get('delivery_date')
                else None,
                delivery_address=data.get('delivery_address'),
                notes=data.get('notes'),
            )

            db.session.add(order)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Order placed successfully',
                'order_id': order.id,
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
