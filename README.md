# Smart Attendance AI

AI-powered facial recognition attendance system built with Flask, OpenCV, and the `face_recognition` library. This project was scaffolded from the Stitch UI blueprint into a runnable full-stack application.

## Features

- Admin authentication (Flask-Login)
- Student management (create, read, update, delete)
- Face registration with webcam capture, validation, and model training
- Live attendance recognition with duplicate-day prevention
- Analytics dashboard with Chart.js
- CSV and Excel attendance export

## Project Structure

```text
.
├── app.py                 # Application entry point
├── config.py              # Environment configuration
├── database.py            # SQLAlchemy, LoginManager, Migrate
├── init_db.py             # Database bootstrap script
├── requirements.txt
├── app/
│   └── __init__.py        # Flask app factory
├── models/
│   └── models.py          # Admin, Student, Attendance, ActivityLog
├── routes/
│   ├── admin.py
│   ├── student.py
│   ├── recognition.py
│   └── analytics.py
├── services/
│   └── face_engine.py
├── templates/
├── static/
├── datasets/              # Face image datasets per student
└── uploads/               # General uploads
```

## Prerequisites

- Python 3.10 or 3.11 recommended
- Webcam for face registration and live attendance
- Windows users may need:
  - [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - [CMake](https://cmake.org/download/) for building `dlib` (required by `face_recognition`)

## Setup

### 1. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `face-recognition` fails to install on Windows, install CMake and Build Tools first, then retry.

### 3. Initialize the database

```bash
python init_db.py
```

Default admin credentials:

- **Username:** `admin`
- **Password:** `admin123`

Change these immediately for any non-local deployment.

### 4. Run the application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Usage Workflow

1. Log in as admin.
2. Go to **Students** and add student records.
3. Open **Register Face** for a student and capture several angles.
4. Click **Finalize Registration** to train encodings.
5. Open **Live Attendance** and start scanning to mark attendance automatically.
6. View trends and export reports under **Reports**.

## Configuration

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_CONFIG` | `development`, `production`, or `testing` | `development` |
| `SECRET_KEY` | Flask secret key | dev placeholder |
| `DATABASE_URL` | SQLAlchemy database URI | SQLite file in project root |
| `PORT` | HTTP port | `5000` |

## API Routes (authenticated)

| Route | Method | Purpose |
|-------|--------|---------|
| `/admin/login` | GET/POST | Admin login |
| `/admin/dashboard` | GET | Dashboard |
| `/students/` | GET | List students |
| `/students/create` | GET/POST | Create student |
| `/ai/register/<id>` | GET | Face registration UI |
| `/ai/upload_face/<id>` | POST | Upload captured face image |
| `/ai/complete_registration/<id>` | POST | Train face model |
| `/ai/live_feed` | GET | Live recognition UI |
| `/ai/process_frame` | POST | Process webcam frame |
| `/analytics/dashboard_data` | GET | Analytics JSON |
| `/analytics/export/csv` | GET | CSV export |
| `/analytics/export/excel` | GET | Excel export |

## Production Notes

- Set a strong `SECRET_KEY` and `DATABASE_URL` (PostgreSQL recommended).
- Use HTTPS so browser camera APIs work reliably outside localhost.
- Run with a WSGI server such as Gunicorn behind a reverse proxy.
- Back up `datasets/` and `static/encodings.pickle`.

## Troubleshooting

- **Camera not working:** Allow camera permissions in the browser; use `localhost` or HTTPS.
- **No matches during live scan:** Ensure face registration was finalized and at least one encoding exists.
- **`face_recognition` install errors:** Install CMake and C++ build tools, then reinstall requirements.

## License

Internal / portfolio project scaffold.
