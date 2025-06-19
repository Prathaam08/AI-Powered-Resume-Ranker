from flask import Flask
from config import Config
from .routes import bp as main_bp
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    # ✅ Makes 'now' available in all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    # ✅ Register your main blueprint
    app.register_blueprint(main_bp)

    return app
