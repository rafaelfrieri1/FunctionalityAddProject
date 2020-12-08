from flask import Flask

def init_app():
    """Initialize the core application"""

    app = Flask(__name__, instance_relative_config = False)
    app.config.from_object('config.Config')

    with app.app_context():
        
        from .Test import Test
        from .popular_skills import popular_skills

        app.register_blueprint(Test.test_bp)
        app.register_blueprint(popular_skills.popular_skills_bp)

        return app