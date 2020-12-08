from flask import Flask

def init_app():
    """Initialize the core application"""

    app = Flask(__name__, instance_relative_config = False)
    app.config.from_object('config.Config')

    with app.app_context():
        
        from .Test import Test

        app.register_blueprint(Test.test_bp)

        return app