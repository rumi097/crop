"""Farmer portal routes: recommendations, listings, costs, labor, equipment, weather, orders."""

import json
import os
from datetime import datetime

import requests
from flask import jsonify, request

from models.database import (
    db,
    User,
    UserRole,
    CropListing,
    CostRecord,
    LaborHiring,
    Equipment,
    RecommendationHistory,
    Order,
    OrderStatus,
)
from utils.auth import role_required, get_current_user
from services.ml_models import load_models, crop_model, fertilizer_model

# Weather API configuration (kept close to weather endpoint)
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your-api-key')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'


def register_farmer_routes(app):
    """Register all farmer-related routes on the given Flask app."""

    @app.route('/api/farmer/crop-recommendation', methods=['POST'])
    @role_required(UserRole.FARMER)
    def farmer_crop_recommendation():
        """Get crop recommendation for farmer"""
        try:
            load_models()
            data = request.json

            required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'pH', 'rainfall']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400

            if crop_model is None:
                return jsonify({'error': 'Crop model not loaded'}), 500

            features = [
                float(data['N']), float(data['P']), float(data['K']),
                float(data['temperature']), float(data['humidity']),
                float(data['pH']), float(data['rainfall'])
            ]

            recommendation = crop_model.predict(features)

            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if user.farmer_profile:
                history = RecommendationHistory(
                    farmer_id=user.farmer_profile.id,
                    recommendation_type='crop',
                    input_parameters=json.dumps(data),
                    recommendation_result=json.dumps(recommendation)
                )
                db.session.add(history)
                db.session.commit()

            return jsonify({'success': True, 'recommendation': recommendation})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/fertilizer-recommendation', methods=['POST'])
    @role_required(UserRole.FARMER)
    def farmer_fertilizer_recommendation():
        """Get fertilizer recommendation for farmer"""
        try:
            load_models()
            data = request.json

            required_fields = ['soil_type', 'crop_type', 'N', 'P', 'K']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400

            if fertilizer_model is None:
                return jsonify({'error': 'Fertilizer model not loaded'}), 500

            recommendation = fertilizer_model.predict({
                'soil_type': data['soil_type'],
                'crop': data['crop_type'],
                'N': float(data['N']),
                'P': float(data['P']),
                'K': float(data['K']),
            })

            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if user.farmer_profile:
                history = RecommendationHistory(
                    farmer_id=user.farmer_profile.id,
                    recommendation_type='fertilizer',
                    input_parameters=json.dumps(data),
                    recommendation_result=json.dumps(recommendation)
                )
                db.session.add(history)
                db.session.commit()

            return jsonify({'success': True, 'recommendation': recommendation})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/recommendation-history', methods=['GET'])
    @role_required(UserRole.FARMER)
    def get_recommendation_history():
        """Get farmer's recommendation history"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            history = RecommendationHistory.query.filter_by(
                farmer_id=user.farmer_profile.id
            ).order_by(RecommendationHistory.created_at.desc()).limit(50).all()

            results = []
            for record in history:
                results.append({
                    'id': record.id,
                    'type': record.recommendation_type,
                    'input': json.loads(record.input_parameters),
                    'result': json.loads(record.recommendation_result),
                    'date': record.created_at.isoformat()
                })

            return jsonify({'success': True, 'history': results})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/crop-listings', methods=['GET', 'POST'])
    @role_required(UserRole.FARMER)
    def farmer_crop_listings():
        """Get or create farmer's crop listings"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            if request.method == 'GET':
                listings = CropListing.query.filter_by(
                    farmer_id=user.farmer_profile.id
                ).order_by(CropListing.created_at.desc()).all()

                return jsonify({
                    'success': True,
                    'listings': [listing.to_dict() for listing in listings]
                })

            data = request.json
            required_fields = ['crop_name', 'quantity', 'price_per_unit']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400

            listing = CropListing(
                farmer_id=user.farmer_profile.id,
                crop_name=data['crop_name'],
                category=data.get('category', 'others'),
                quantity=float(data['quantity']),
                unit=data.get('unit', 'kg'),
                price_per_unit=float(data['price_per_unit']),
                location=data.get('location'),
                description=data.get('description'),
                image_url=data.get('image_url'),
                harvest_date=datetime.strptime(data['harvest_date'], '%Y-%m-%d').date() if data.get('harvest_date') else None
            )

            db.session.add(listing)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Crop listing created',
                'listing': listing.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/crop-listings/<int:listing_id>', methods=['PUT', 'DELETE'])
    @role_required(UserRole.FARMER)
    def manage_crop_listing(listing_id):
        """Update or delete crop listing"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            listing = CropListing.query.get(listing_id)
            if not listing or listing.farmer_id != user.farmer_profile.id:
                return jsonify({'error': 'Listing not found'}), 404

            if request.method == 'PUT':
                data = request.json
                if 'quantity' in data:
                    listing.quantity = float(data['quantity'])
                if 'price_per_unit' in data:
                    listing.price_per_unit = float(data['price_per_unit'])
                if 'is_available' in data:
                    listing.is_available = bool(data['is_available'])
                if 'location' in data:
                    listing.location = data['location']
                if 'description' in data:
                    listing.description = data['description']

                db.session.commit()
                return jsonify({'success': True, 'listing': listing.to_dict()})

            db.session.delete(listing)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Listing deleted'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/costs', methods=['GET', 'POST'])
    @role_required(UserRole.FARMER)
    def farmer_costs():
        """Get or create cost records"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            if request.method == 'GET':
                records = CostRecord.query.filter_by(
                    farmer_id=user.farmer_profile.id
                ).order_by(CostRecord.created_at.desc()).all()

                results = []
                for record in records:
                    results.append({
                        'id': record.id,
                        'crop_name': record.crop_name,
                        'season': record.season,
                        'year': record.year,
                        'costs': {
                            'seed': record.seed_cost,
                            'fertilizer': record.fertilizer_cost,
                            'pesticide': record.pesticide_cost,
                            'labor': record.labor_cost,
                            'equipment': record.equipment_cost,
                            'irrigation': record.irrigation_cost,
                            'other': record.other_cost,
                            'total': record.total_cost
                        },
                        'revenue': record.revenue,
                        'profit_loss': record.profit_loss,
                        'notes': record.notes
                    })

                return jsonify({'success': True, 'records': results})

            data = request.json

            total_cost = (
                float(data.get('seed_cost', 0)) +
                float(data.get('fertilizer_cost', 0)) +
                float(data.get('pesticide_cost', 0)) +
                float(data.get('labor_cost', 0)) +
                float(data.get('equipment_cost', 0)) +
                float(data.get('irrigation_cost', 0)) +
                float(data.get('other_cost', 0))
            )

            revenue = float(data.get('revenue', 0))
            profit_loss = revenue - total_cost

            record = CostRecord(
                farmer_id=user.farmer_profile.id,
                crop_name=data['crop_name'],
                season=data.get('season'),
                year=int(data['year']),
                seed_cost=float(data.get('seed_cost', 0)),
                fertilizer_cost=float(data.get('fertilizer_cost', 0)),
                pesticide_cost=float(data.get('pesticide_cost', 0)),
                labor_cost=float(data.get('labor_cost', 0)),
                equipment_cost=float(data.get('equipment_cost', 0)),
                irrigation_cost=float(data.get('irrigation_cost', 0)),
                other_cost=float(data.get('other_cost', 0)),
                total_cost=total_cost,
                revenue=revenue,
                profit_loss=profit_loss,
                notes=data.get('notes')
            )

            db.session.add(record)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Cost record created',
                'record_id': record.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/labor-postings', methods=['GET', 'POST'])
    @role_required(UserRole.FARMER)
    def farmer_labor_postings():
        """Get or create labor hiring postings"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            if request.method == 'GET':
                postings = LaborHiring.query.filter_by(
                    farmer_id=user.farmer_profile.id
                ).order_by(LaborHiring.created_at.desc()).all()

                results = []
                for posting in postings:
                    labor_user = User.query.get(posting.labor.user_id) if posting.labor else None
                    results.append({
                        'id': posting.id,
                        'job_title': posting.job_title,
                        'description': posting.description,
                        'work_type': posting.work_type,
                        'start_date': posting.start_date.isoformat(),
                        'end_date': posting.end_date.isoformat() if posting.end_date else None,
                        'total_days': posting.total_days,
                        'wage_per_day': posting.daily_wage,
                        'total_wage': posting.total_wage,
                        'status': posting.status,
                        'location': posting.location,
                        'laborers_needed': posting.laborers_needed,
                        'labor_name': labor_user.full_name if labor_user else None,
                        'labor_phone': labor_user.phone if labor_user else None
                    })

                return jsonify({'success': True, 'postings': results})

            data = request.json

            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None

            total_days = (end_date - start_date).days + 1 if end_date else None

            posting = LaborHiring(
                farmer_id=user.farmer_profile.id,
                labor_id=data.get('labor_id'),
                job_title=data['job_title'],
                description=data.get('description'),
                work_type=data.get('work_type'),
                start_date=start_date,
                end_date=end_date,
                total_days=total_days,
                daily_wage=float(data['wage_per_day']) if data.get('wage_per_day') else None,
                total_wage=float(data['total_wage']) if data.get('total_wage') else None,
                location=data.get('location'),
                laborers_needed=int(data.get('laborers_needed', 1)),
                status='open'
            )

            db.session.add(posting)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Labor posting created',
                'posting_id': posting.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/labor-postings/<int:posting_id>', methods=['PUT'])
    @role_required(UserRole.FARMER)
    def manage_labor_posting(posting_id):
        """Update an existing labor posting (details or status)."""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            posting = LaborHiring.query.get(posting_id)
            if not posting or posting.farmer_id != user.farmer_profile.id:
                return jsonify({'error': 'Labor posting not found'}), 404

            data = request.json or {}

            if 'job_title' in data:
                posting.job_title = data['job_title']
            if 'description' in data:
                posting.description = data['description']
            if 'work_type' in data:
                posting.work_type = data['work_type']
            if 'start_date' in data:
                posting.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            if 'end_date' in data:
                posting.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data['end_date'] else None

            if posting.start_date and posting.end_date:
                posting.total_days = (posting.end_date - posting.start_date).days + 1

            if 'wage_per_day' in data:
                posting.daily_wage = float(data['wage_per_day']) if data['wage_per_day'] is not None else None
            if 'total_wage' in data:
                posting.total_wage = float(data['total_wage']) if data['total_wage'] is not None else posting.total_wage
            if 'location' in data:
                posting.location = data['location']
            if 'laborers_needed' in data:
                posting.laborers_needed = int(data['laborers_needed'])
            if 'status' in data:
                if data['status'] in ['open', 'active', 'completed', 'cancelled']:
                    posting.status = data['status']
                else:
                    return jsonify({'error': 'Invalid status value'}), 400

            db.session.commit()

            labor_user = User.query.get(posting.labor.user_id) if posting.labor else None
            result = {
                'id': posting.id,
                'job_title': posting.job_title,
                'description': posting.description,
                'work_type': posting.work_type,
                'start_date': posting.start_date.isoformat(),
                'end_date': posting.end_date.isoformat() if posting.end_date else None,
                'total_days': posting.total_days,
                'wage_per_day': posting.daily_wage,
                'total_wage': posting.total_wage,
                'status': posting.status,
                'location': posting.location,
                'laborers_needed': posting.laborers_needed,
                'labor_name': labor_user.full_name if labor_user else None,
                'labor_phone': labor_user.phone if labor_user else None
            }

            return jsonify({'success': True, 'posting': result})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/equipment', methods=['GET', 'POST'])
    @role_required(UserRole.FARMER)
    def farmer_equipment():
        """Get or create equipment"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            if request.method == 'GET':
                equipment = Equipment.query.filter_by(
                    owner_id=user.farmer_profile.id
                ).all()

                results = []
                for item in equipment:
                    results.append({
                        'id': item.id,
                        'equipment_name': item.equipment_name,
                        'equipment_type': item.equipment_type,
                        'description': item.description,
                        'rental_price_per_day': item.rental_price_per_day,
                        'is_available_for_rent': item.is_available_for_rent,
                        'is_available_for_share': item.is_available_for_share,
                        'condition': item.condition
                    })

                return jsonify({'success': True, 'equipment': results})

            data = request.json

            equipment = Equipment(
                owner_id=user.farmer_profile.id,
                equipment_name=data['equipment_name'],
                equipment_type=data.get('equipment_type'),
                description=data.get('description'),
                rental_price_per_day=float(data.get('rental_price_per_day', 0)),
                is_available_for_rent=data.get('is_available_for_rent', False),
                is_available_for_share=data.get('is_available_for_share', False),
                condition=data.get('condition', 'good')
            )

            db.session.add(equipment)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Equipment added',
                'equipment_id': equipment.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/weather', methods=['GET'])
    @role_required(UserRole.FARMER)
    def get_weather():
        """Get weather information for farmer's location"""
        try:
            location = request.args.get('location')
            if not location:
                return jsonify({'error': 'Location parameter required'}), 400

            if WEATHER_API_KEY == 'your-api-key' or not WEATHER_API_KEY:
                return jsonify({
                    'success': True,
                    'weather': {
                        'temperature': 25.0,
                        'humidity': 65,
                        'description': 'Clear sky (demo data)',
                        'wind_speed': 3.5,
                        'pressure': 1013
                    }
                })

            params = {
                'q': location,
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            }

            response = requests.get(WEATHER_API_URL, params=params, timeout=5)

            if response.status_code == 200:
                weather_data = response.json()
                return jsonify({
                    'success': True,
                    'weather': {
                        'temperature': weather_data['main']['temp'],
                        'humidity': weather_data['main']['humidity'],
                        'description': weather_data['weather'][0]['description'],
                        'wind_speed': weather_data['wind']['speed'],
                        'pressure': weather_data['main']['pressure']
                    }
                })
            return jsonify({'error': 'Weather data not available'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/orders', methods=['GET'])
    @role_required(UserRole.FARMER)
    def farmer_orders():
        """Get orders for this farmer's crop listings and allow them to track status."""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            orders = (
                Order.query
                .join(CropListing, Order.crop_listing_id == CropListing.id)
                .filter(
                    Order.order_type == 'crop',
                    CropListing.farmer_id == user.farmer_profile.id
                )
                .order_by(Order.created_at.desc())
                .all()
            )

            results = []
            for order in orders:
                buyer = User.query.get(order.buyer_id)
                results.append({
                    'id': order.id,
                    'order_type': order.order_type,
                    'crop_listing_id': order.crop_listing_id,
                    'product_name': order.crop_listing.crop_name if order.crop_listing else None,
                    'buyer_name': buyer.full_name if buyer else 'Unknown',
                    'buyer_email': buyer.email if buyer else None,
                    'quantity': order.quantity,
                    'unit_price': order.unit_price,
                    'total_price': order.total_price,
                    'status': order.status.value,
                    'delivery_date': order.delivery_date.isoformat() if order.delivery_date else None,
                    'created_at': order.created_at.isoformat(),
                })

            return jsonify({'success': True, 'orders': results})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/farmer/orders/<int:order_id>/status', methods=['PUT'])
    @role_required(UserRole.FARMER)
    def update_farmer_order_status(order_id):
        """Allow farmer to update the status of an order for their crop listing."""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.farmer_profile:
                return jsonify({'error': 'Farmer profile not found'}), 404

            order = Order.query.get(order_id)
            if not order or order.order_type != 'crop' or not order.crop_listing:
                return jsonify({'error': 'Order not found'}), 404

            if order.crop_listing.farmer_id != user.farmer_profile.id:
                return jsonify({'error': 'Not authorized to update this order'}), 403

            data = request.json or {}
            new_status = data.get('status')
            if not new_status:
                return jsonify({'error': 'Status is required'}), 400

            try:
                order.status = OrderStatus(new_status)
            except ValueError:
                return jsonify({'error': 'Invalid status value'}), 400

            db.session.commit()

            return jsonify({
                'success': True,
                'order': {
                    'id': order.id,
                    'status': order.status.value
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

