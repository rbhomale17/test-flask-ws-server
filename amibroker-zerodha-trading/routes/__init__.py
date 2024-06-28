from .order import create_order_blueprint
from .profile import create_profile_blueprint
# from .auth import create_auth_blueprint
from .gtt import create_gtt_blueprint
# from .trades import create_trades_blueprint
from .index import index_blueprint
from .log import create_log_blueprint

def register_blueprints(app, db, kite):
    app.register_blueprint(create_order_blueprint(db, kite))
    app.register_blueprint(create_profile_blueprint(db, kite))
    # app.register_blueprint(create_auth_blueprint(db, kite))
    app.register_blueprint(create_gtt_blueprint(db, kite))
    # app.register_blueprint(create_trades_blueprint(db, kite))
    app.register_blueprint(index_blueprint(db, kite))
    app.register_blueprint(create_log_blueprint(db,kite))
