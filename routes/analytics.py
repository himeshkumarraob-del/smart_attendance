import io
from datetime import datetime, timedelta

import pandas as pd
from flask import Blueprint, jsonify, render_template, send_file
from flask_login import login_required
from sqlalchemy import func

from database import db
from models.models import Attendance, Student

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/')
@login_required
def reports():
    return render_template('analytics/reports.html')


@analytics_bp.route('/dashboard_data')
@login_required
def dashboard_data():
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=29)

    trends = (
        db.session.query(Attendance.attendance_date, func.count(Attendance.id))
        .filter(Attendance.attendance_date >= start_date)
        .group_by(Attendance.attendance_date)
        .order_by(Attendance.attendance_date)
        .all()
    )

    dept_stats = (
        db.session.query(Student.department, func.count(Attendance.id))
        .join(Attendance, Student.id == Attendance.student_id_ref)
        .group_by(Student.department)
        .all()
    )

    rankings = (
        db.session.query(Student.name, func.count(Attendance.id).label('total'))
        .join(Attendance, Student.id == Attendance.student_id_ref)
        .group_by(Student.id)
        .order_by(func.count(Attendance.id).desc())
        .limit(10)
        .all()
    )

    total_students = Student.query.count()
    today_count = Attendance.query.filter_by(attendance_date=end_date).count()
    avg_rate = round((today_count / total_students * 100), 1) if total_students else 0.0

    return jsonify({
        'trends': [{'date': str(d), 'count': c} for d, c in trends],
        'departments': [{'name': n or 'Unassigned', 'count': c} for n, c in dept_stats],
        'rankings': [{'name': n, 'count': c} for n, c in rankings],
        'summary': {
            'total_students': total_students,
            'present_today': today_count,
            'attendance_rate': avg_rate,
        },
    })


@analytics_bp.route('/export/<format>')
@login_required
def export_attendance(format):
    rows = (
        db.session.query(
            Attendance.attendance_date,
            Attendance.attendance_time,
            Student.name,
            Student.roll_number,
            Student.department,
            Attendance.status,
            Attendance.confidence_score,
        )
        .join(Student, Attendance.student_id_ref == Student.id)
        .order_by(Attendance.attendance_date.desc(), Attendance.attendance_time.desc())
        .all()
    )

    df = pd.DataFrame(
        rows,
        columns=[
            'Date', 'Time', 'Name', 'Roll Number',
            'Department', 'Status', 'Confidence',
        ],
    )
    output = io.BytesIO()

    if format == 'csv':
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name='attendance_report.csv',
        )

    if format == 'excel':
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Attendance')
        output.seek(0)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='attendance_report.xlsx',
        )

    return jsonify({'error': 'Invalid format. Use csv or excel.'}), 400
