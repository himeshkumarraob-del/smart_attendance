import os

from flask import Flask, redirect, url_for

from config import config
from database import db, login_manager, migrate


def create_app(config_name='default'):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static'),
    )
    app.config.from_object(config[config_name])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DATASET_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'static', 'encodings'), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    import models.models  # noqa: F401

    from routes.admin import admin_bp
    from routes.analytics import analytics_bp
    from routes.recognition import recognition_bp
    from routes.student import student_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/students')
    app.register_blueprint(recognition_bp, url_prefix='/ai')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')

    @app.route('/')
    def index():
        return redirect(url_for('admin.login'))

    return app
