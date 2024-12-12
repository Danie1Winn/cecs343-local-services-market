from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from werkzeug.security import generate_password_hash
from app import db
from app.models.worker import Worker
from app.models.employer import Employer

developer_bp = Blueprint('developer', __name__, url_prefix='/developer')

@developer_bp.route('/dashboard')
def dashboard():
    if session.get('role') not in ['developer', 'developer_worker', 'developer_employer']:
        abort(403)  # Access forbidden for non-developers
    return render_template('developer_dashboard.html')

@developer_bp.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if session.get('role') not in ['developer', 'developer_worker', 'developer_employer']:
        abort(403)

    if request.method == 'POST':
        account_type = request.form['account_type']
        name = request.form['name']
        phone_number = request.form['phone_number']
        password = request.form['password']

        # Default values for worker-specific fields
        zip_code = request.form.get('zip_code', '00000')
        travel_distance = request.form.get('travel_distance', 10)

        hashed_password = generate_password_hash(password)  # Generate hashed password

        if account_type == 'worker':
            new_worker = Worker(
                name=name,
                phone_number=phone_number,
                password=hashed_password,
                zip_code=zip_code,
                travel_distance=travel_distance,
                user_role='regular'
            )
            db.session.add(new_worker)
        elif account_type == 'employer':
            new_employer = Employer(
                name=name,
                phone_number=phone_number,
                password=hashed_password,
                user_role='regular'
            )
            db.session.add(new_employer)

        db.session.commit()
        flash('Test account created successfully!', 'success')
        return redirect(url_for('developer.dashboard'))

    return render_template('create_test_account.html')

@developer_bp.route('/test_accounts')
def view_test_accounts():
    if session.get('role') not in ['developer', 'developer_worker', 'developer_employer']:
        abort(403)

    workers = Worker.query.all()
    employers = Employer.query.all()

    return render_template('test_accounts.html', workers=workers, employers=employers)

@developer_bp.route('/remove_account/<int:account_id>/<string:account_type>', methods=['POST'])
def remove_account(account_id, account_type):
    if session.get('role') != 'developer':
        abort(403)

    if account_type == 'worker':
        account = Worker.query.get_or_404(account_id)
    elif account_type == 'employer':
        account = Employer.query.get_or_404(account_id)
    else:
        flash("Invalid account type.", "danger")
        return redirect(url_for('developer.view_test_accounts'))

    db.session.delete(account)
    db.session.commit()
    flash(f"{account_type.capitalize()} account removed successfully!", "success")
    return redirect(url_for('developer.view_test_accounts'))

@developer_bp.route('/session-debug')
def session_debug():
    """Debugging route to display current session data."""
    if session.get('role') != 'developer':
        abort(403)

    return {
        "session_data": dict(session)  # Displays session data for debugging purposes
    }
