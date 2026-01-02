"""Labor portal routes: job postings and applications."""

from flask import jsonify

from models.database import User, UserRole, LaborHiring
from utils.auth import role_required, get_current_user


def register_labor_routes(app):
    """Register all labor-related routes on the given Flask app."""

    @app.route('/api/labor/job-postings', methods=['GET'])
    @role_required(UserRole.LABOR)
    def labor_job_postings():
        """Get available job postings for labor"""
        try:
            postings = (
                LaborHiring.query
                .filter_by(status='open')
                .order_by(LaborHiring.created_at.desc())
                .all()
            )

            results = []
            for posting in postings:
                farmer_user = User.query.get(posting.farmer.user_id)
                results.append({
                    'id': posting.id,
                    'farmer_name': farmer_user.full_name if farmer_user else 'Unknown',
                    'farmer_location': posting.farmer.farm_location,
                    'job_title': posting.job_title,
                    'description': posting.description,
                    'work_type': posting.work_type,
                    'start_date': posting.start_date.isoformat(),
                    'end_date': posting.end_date.isoformat() if posting.end_date else None,
                    'wage_per_day': posting.daily_wage,
                    'total_wage': posting.total_wage,
                    'location': posting.location,
                    'laborers_needed': posting.laborers_needed,
                    'total_days': posting.total_days,
                })

            return jsonify({'success': True, 'postings': results})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/labor/apply/<int:posting_id>', methods=['POST'])
    @role_required(UserRole.LABOR)
    def labor_apply_job(posting_id):
        """Apply for a job posting"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.labor_profile:
                return jsonify({'error': 'Labor profile not found'}), 404

            posting = LaborHiring.query.get(posting_id)
            if not posting:
                return jsonify({'error': 'Job posting not found'}), 404

            if posting.labor_id:
                return jsonify({'error': 'Job already taken'}), 400

            posting.labor_id = user.labor_profile.id
            db.session.commit()

            return jsonify({'success': True, 'message': 'Application successful'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/labor/my-jobs', methods=['GET'])
    @role_required(UserRole.LABOR)
    def labor_my_jobs():
        """Get labor's current and past jobs"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])

            if not user.labor_profile:
                return jsonify({'error': 'Labor profile not found'}), 404

            jobs = (
                LaborHiring.query
                .filter_by(labor_id=user.labor_profile.id)
                .order_by(LaborHiring.created_at.desc())
                .all()
            )

            results = []
            for job in jobs:
                farmer_user = User.query.get(job.farmer.user_id)
                results.append({
                    'id': job.id,
                    'farmer_name': farmer_user.full_name if farmer_user else 'Unknown',
                    'job_title': job.job_title,
                    'work_type': job.work_type,
                    'start_date': job.start_date.isoformat(),
                    'end_date': job.end_date.isoformat() if job.end_date else None,
                    'daily_wage': job.daily_wage,
                    'total_wage': job.total_wage,
                    'status': job.status,
                })

            return jsonify({'success': True, 'jobs': results})

        except Exception as e:
            return jsonify({'error': str(e)}), 500
