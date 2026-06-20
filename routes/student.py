from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import or_

from database import db
from models.models import ActivityLog, Attendance, Student

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
@login_required
def list_students():
    query = request.args.get('q', '').strip()
    dept = request.args.get('dept', '').strip()

    students_query = Student.query

    if query:
        like = f'%{query}%'
        students_query = students_query.filter(
            or_(
                Student.name.ilike(like),
                Student.roll_number.ilike(like),
                Student.student_id.ilike(like),
            )
        )

    if dept:
        students_query = students_query.filter(Student.department == dept)

    students = students_query.order_by(Student.name.asc()).all()
    departments = [
        row[0]
        for row in db.session.query(Student.department)
        .filter(Student.department.isnot(None), Student.department != '')
        .distinct()
        .order_by(Student.department)
        .all()
    ]

    return render_template(
        'student/list.html',
        students=students,
        departments=departments,
        query=query,
        dept=dept,
    )


@student_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        department = request.form.get('department', '').strip() or None
        email = request.form.get('email', '').strip() or None

        if not student_id or not name or not roll_number:
            flash('Student ID, name, and roll number are required.', 'error')
            return render_template('student/form.html', student=None)

        existing = Student.query.filter(
            or_(
                Student.student_id == student_id,
                Student.roll_number == roll_number,
            )
        ).first()
        if existing:
            flash('A student with that ID or roll number already exists.', 'error')
            return render_template('student/form.html', student=None)

        student = Student(
            student_id=student_id,
            name=name,
            roll_number=roll_number,
            department=department,
            email=email,
        )
        db.session.add(student)
        db.session.add(ActivityLog(action=f"Created student: {student.name}"))
        db.session.commit()
        flash('Student created successfully.', 'success')
        return redirect(url_for('student.list_students'))

    return render_template('student/form.html', student=None)


@student_bp.route('/<int:student_id>')
@login_required
def profile(student_id):
    student = db.get_or_404(Student, student_id)
    attendances = (
        student.attendances.order_by(
            Attendance.attendance_date.desc(),
            Attendance.attendance_time.desc(),
        )
        .limit(30)
        .all()
    )
    return render_template(
        'student/profile.html',
        student=student,
        attendances=attendances,
    )


@student_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(student_id):
    student = db.get_or_404(Student, student_id)

    if request.method == 'POST':
        student.name = request.form.get('name', '').strip()
        student.roll_number = request.form.get('roll_number', '').strip()
        student.department = request.form.get('department', '').strip() or None
        student.email = request.form.get('email', '').strip() or None

        if not student.name or not student.roll_number:
            flash('Name and roll number are required.', 'error')
            return render_template('student/form.html', student=student)

        duplicate = Student.query.filter(
            Student.id != student.id,
            Student.roll_number == student.roll_number,
        ).first()
        if not duplicate and student.email:
            duplicate = Student.query.filter(
                Student.id != student.id,
                Student.email == student.email,
            ).first()
        if duplicate:
            flash('Another student already uses that roll number or email.', 'error')
            return render_template('student/form.html', student=student)

        db.session.add(ActivityLog(action=f"Updated student: {student.name}"))
        db.session.commit()
        flash('Student updated successfully.', 'success')
        return redirect(url_for('student.profile', student_id=student.id))

    return render_template('student/form.html', student=student)


@student_bp.route('/<int:student_id>/delete', methods=['POST'])
@login_required
def delete(student_id):
    student = db.get_or_404(Student, student_id)
    name = student.name
    db.session.delete(student)
    db.session.add(ActivityLog(action=f"Deleted student: {name}"))
    db.session.commit()
    flash(f'Student "{name}" deleted.', 'success')
    return redirect(url_for('student.list_students'))
