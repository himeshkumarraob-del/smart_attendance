"""Initialize database tables and default admin account."""

from app import create_app
from database import db
from models.models import Admin


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()

        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Default admin created.')
            print('Username: admin')
            print('Password: admin123')
        else:
            print('Admin account already exists.')


if __name__ == '__main__':
    init_db()
