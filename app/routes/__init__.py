from .auth import auth_bp
from .users import user_bp
from .shops import shop_bp
from .bookings import booking_bp
from .workers import worker_bp
from .reviews import review_bp
from .analytics import analytics_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(analytics_bp)
