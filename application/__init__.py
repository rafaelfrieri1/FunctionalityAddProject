from flask import Flask

def init_app():
    """Initialize the core application"""

    app = Flask(__name__, instance_relative_config = False)
    app.config.from_object('config.Config')

    with app.app_context():
        
        from .Test import Test
        from .popular_skills import popular_skills
        from .strength_based_search import strength_based_search
        from .target_audiences_platform_enhance import target_audiences_platform_enhance

        app.register_blueprint(Test.test_bp)
        app.register_blueprint(popular_skills.popular_skills_bp)
        app.register_blueprint(strength_based_search.strength_based_search_bp)
        app.register_blueprint(target_audiences_platform_enhance.target_audiences_platform_enhance_bp)

        return app