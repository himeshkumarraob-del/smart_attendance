import os
import pickle

import cv2
import face_recognition
import numpy as np
from flask import current_app

from database import db
from models.models import Student


class FaceEngine:
    def __init__(self):
        self.known_encodings = []
        self.known_ids = []
        self.encoding_file = None

    def _encoding_path(self):
        if self.encoding_file is None:
            self.encoding_file = current_app.config['ENCODINGS_FILE']
        return self.encoding_file

    def load_encodings(self):
        path = self._encoding_path()
        if os.path.exists(path):
            with open(path, 'rb') as handle:
                data = pickle.load(handle)
                self.known_encodings = data.get('encodings', [])
                self.known_ids = data.get('ids', [])
        else:
            self.train_all_faces()

    def train_all_faces(self):
        dataset_root = current_app.config['DATASET_FOLDER']
        all_encodings = []
        all_ids = []

        for student in Student.query.all():
            student_dir = os.path.join(dataset_root, student.student_id)
            if not os.path.isdir(student_dir):
                continue

            for filename in os.listdir(student_dir):
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue

                filepath = os.path.join(student_dir, filename)
                image = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    all_encodings.append(encodings[0])
                    all_ids.append(student.id)

        os.makedirs(os.path.dirname(self._encoding_path()), exist_ok=True)
        with open(self._encoding_path(), 'wb') as handle:
            pickle.dump({'encodings': all_encodings, 'ids': all_ids}, handle)

        self.known_encodings = all_encodings
        self.known_ids = all_ids
        return len(all_ids)

    def recognize_face(self, frame_bgr):
        if not self.known_encodings:
            self.load_encodings()

        rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        results = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            student_id = None
            confidence = 0.0

            if self.known_encodings:
                face_distances = face_recognition.face_distance(
                    self.known_encodings,
                    face_encoding,
                )
                best_match_index = int(np.argmin(face_distances))
                matches = face_recognition.compare_faces(
                    self.known_encodings,
                    face_encoding,
                    tolerance=0.6,
                )

                if matches[best_match_index]:
                    student_id = self.known_ids[best_match_index]
                    confidence = round((1 - face_distances[best_match_index]) * 100, 2)

            results.append({
                'location': (top, right, bottom, left),
                'student_id': student_id,
                'confidence': confidence,
                'unknown': student_id is None,
            })

        return results
