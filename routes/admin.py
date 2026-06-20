from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func

from database import db
from models.models import ActivityLog, Admin, Attendance, Student

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            login_user(admin)
            db.session.add(ActivityLog(action=f"Admin '{username}' logged in successfully."))
            db.session.commit()

            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))

        flash('Invalid username or password.', 'error')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    db.session.add(ActivityLog(action=f"Admin '{username}' logged out."))
    db.session.commit()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    total_students = Student.query.count()
    present_today = Attendance.query.filter_by(attendance_date=today).count()
    attendance_rate = round((present_today / total_students * 100), 1) if total_students else 0.0

    recent_attendance = (
        Attendance.query.filter_by(attendance_date=today)
        .join(Student)
        .order_by(Attendance.attendance_time.desc())
        .limit(10)
        .all()
    )

    recent_logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(8).all()

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        present_today=present_today,
        attendance_rate=attendance_rate,
        recent_attendance=recent_attendance,
        recent_logs=recent_logs,
    )
