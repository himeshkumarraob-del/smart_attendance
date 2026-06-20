from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from database import db, login_manager


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, int(user_id))


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    image_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attendances = db.relationship(
        'Attendance',
        backref='student',
        lazy='dynamic',
        cascade='all, delete-orphan',
    )

    def face_image_count(self):
        from flask import current_app
        import os

        student_dir = os.path.join(
            current_app.config['DATASET_FOLDER'],
            self.student_id,
        )
        if not os.path.isdir(student_dir):
            return 0
        return len([
            f for f in os.listdir(student_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

    def is_face_registered(self):
        return self.face_image_count() >= 1


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id_ref = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    attendance_date = db.Column(db.Date, default=datetime.utcnow().date)
    attendance_time = db.Column(db.Time, default=datetime.utcnow().time)
    status = db.Column(db.String(20), default='Present')
    confidence_score = db.Column(db.Float, nullable=True)


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
