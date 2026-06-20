import base64
import os
from datetime import datetime

import cv2
import numpy as np
from flask import Blueprint, current_app, jsonify, render_template, request
from flask_login import login_required

from database import db
from models.models import ActivityLog, Attendance, Student
from services.face_engine import FaceEngine

recognition_bp = Blueprint('recognition', __name__)
_face_engine = None


def get_face_engine():
    global _face_engine
    if _face_engine is None:
        _face_engine = FaceEngine()
    return _face_engine


def decode_image(image_data):
    _, encoded = image_data.split(',', 1)
    data_bytes = base64.b64decode(encoded)
    nparr = np.frombuffer(data_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


@recognition_bp.route('/register/<int:student_id>')
@login_required
def register_face(student_id):
    student = db.get_or_404(Student, student_id)
    target = current_app.config['FACE_CAPTURE_TARGET']
    captured = student.face_image_count()
    return render_template(
        'recognition/register.html',
        student=student,
        target=target,
        captured=captured,
    )


@recognition_bp.route('/upload_face/<int:student_id>', methods=['POST'])
@login_required
def upload_face(student_id):
    student = db.get_or_404(Student, student_id)
    data = request.get_json(silent=True) or {}
    image_data = data.get('image')
    image_index = data.get('index', 0)

    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        img = decode_image(image_data)
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return jsonify({'error': 'No face detected. Please ensure your face is visible.'}), 400
        if len(faces) > 1:
            return jsonify({'error': 'Multiple faces detected. Only one person should be in the frame.'}), 400

        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        #if laplacian_var < 100:
        #    return jsonify({'error': 'Image is too blurry. Please stay still.'}), 400

        if student.face_image_count() >= current_app.config['FACE_CAPTURE_TARGET']:
            return jsonify({'error': 'MAXIMUM IMAGES REACHED.'}), 400

        student_dir = os.path.join(current_app.config['DATASET_FOLDER'], student.student_id)
        os.makedirs(student_dir, exist_ok=True)

        filename = f"face_{image_index}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(student_dir, filename)
        cv2.imwrite(filepath, img)

        if image_index == 0 or not student.image_path:
            student.image_path = f"{student.student_id}/{filename}"
            db.session.commit()

        return jsonify({
            'success': True,
            'path': filename,
            'count': student.face_image_count(),
        })

    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


@recognition_bp.route('/complete_registration/<int:student_id>', methods=['POST'])
@login_required
def complete_registration(student_id):
    student = db.get_or_404(Student, student_id)

    if student.face_image_count() < 1:
        return jsonify({'error': 'Capture at least one face image before finalizing.'}), 400

    count = get_face_engine().train_all_faces()
    db.session.add(ActivityLog(action=f"Completed face registration for: {student.name}"))
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Registration finalized and model updated.',
        'encodings': count,
    })


@recognition_bp.route('/live_feed')
@login_required
def live_feed():
    return render_template('recognition/live_feed.html')


@recognition_bp.route('/process_frame', methods=['POST'])
@login_required
def process_frame():
    data = request.get_json(silent=True) or {}
    image_data = data.get('image')

    if not image_data:
        return jsonify({'error': 'No image data'}), 400

    try:
        img = decode_image(image_data)
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400

        threshold = current_app.config['RECOGNITION_CONFIDENCE_THRESHOLD']
        matches = get_face_engine().recognize_face(img)
        response_data = []

        for match in matches:
            student_info = None
            if match['student_id']:
                student = db.session.get(Student, match['student_id'])
                if student:
                    student_info = {
                        'name': student.name,
                        'roll': student.roll_number,
                        'dept': student.department,
                        'id': student.id,
                        'student_code': student.student_id,
                    }

                    today = datetime.utcnow().date()
                    existing = Attendance.query.filter_by(
                        student_id_ref=student.id,
                        attendance_date=today,
                    ).first()

                    if not existing and match['confidence'] > threshold:
                        db.session.add(Attendance(
                            student_id_ref=student.id,
                            attendance_date=today,
                            attendance_time=datetime.utcnow().time(),
                            confidence_score=match['confidence'],
                        ))
                        db.session.add(ActivityLog(
                            action=f"Attendance marked for: {student.name} ({match['confidence']}%)"
                        ))
                        db.session.commit()
                        student_info['attendance_marked'] = True
                    elif existing:
                        student_info['attendance_marked'] = False
                        student_info['already_marked'] = True

            response_data.append({
                'location': match['location'],
                'student': student_info,
                'confidence': match['confidence'],
                'unknown': match['unknown'],
            })

        return jsonify({'results': response_data})

    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': str(exc)}), 500


@recognition_bp.route('/retrain', methods=['POST'])
@login_required
def retrain():
    count = get_face_engine().train_all_faces()
    db.session.add(ActivityLog(action=f'Face model retrained ({count} encodings).'))
    db.session.commit()
    return jsonify({'success': True, 'count': count})
