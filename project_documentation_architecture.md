# AI-Powered Smart Attendance System - Project Architecture & Documentation

## 1. Project Overview
A production-grade, full-stack facial recognition attendance system. Designed for high scalability and professional deployment.

## 2. Technical Stack
- **Backend**: Flask (Python) with Blueprint architecture.
- **AI Engine**: OpenCV & face_recognition (HOG/CNN models).
- **Frontend**: HTML5, CSS3, JS (Bootstrap 5 + Tailwind for utilities).
- **Database**: SQLAlchemy ORM (SQLite for dev, PostgreSQL ready).
- **Analytics**: Chart.js for visualization.

## 3. Folder Structure
```text
project_root/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py           # SQLAlchemy database models
│   ├── routes/
│   │   ├── admin.py        # Dashboard & Auth
│   │   ├── student.py      # CRUD Student operations
│   │   └── recognition.py  # AI processing routes
│   ├── services/
│   │   ├── face_engine.py  # Facial encoding & comparison
│   │   └── report_gen.py   # CSV/Excel export logic
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/        # Student face datasets
│   └── templates/          # HTML files
├── config.py               # Environment & App configs
├── requirements.txt        # Python dependencies
├── run.py                  # Entry point
└── README.md               # Setup & Architecture guide
```

## 4. Key Workflows
### Face Registration
1. Admin captures 5-10 images via webcam.
2. `face_engine.py` validates face presence and quality.
3. Images are stored in `uploads/<student_id>/`.
4. Encodings are generated and saved to a pickle file/database for fast lookup.

### Real-time Recognition
1. Live video frames are sent to the recognition route.
2. The AI compares the live encoding against the known dataset.
3. If match found > threshold (e.g. 0.6), attendance is logged in the DB.
4. Duplicate check prevents double marking within the same session.

## 5. Security Measures
- CSRF Protection on all forms.
- Password hashing using Argon2/Bcrypt.
- Secure file upload validators (extension & size checks).
- Role-based route protection.
