import os
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    from tour_flask_app.views.main_views import main_bp

    app.register_blueprint(main_bp, url_prefix='/')

    
    
    return app

