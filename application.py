import matplotlib
matplotlib.use('Agg')

import atexit
from flask import Flask
from flask_cors import CORS
from controller.asset_controller import asset_controller
from controller.asset_manager_controller import asset_manager_controller
from controller.total_balance_controller import total_balance_controller
from asset_manager.asset_manager import AssetManager
from apscheduler.schedulers.background import BackgroundScheduler

def refetchAssets():
    asset_manager = AssetManager("config/config.json", "USDT")
    asset_manager.run()

app = Flask(__name__)
app.register_blueprint(asset_controller)
app.register_blueprint(asset_manager_controller)
app.register_blueprint(total_balance_controller)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/status")
def get_api_status():
    return {"status": "API Up and Running"}, 200

def init_scheduler():
    print("Registering Scheduler")

    scheduler = BackgroundScheduler()

    scheduler.add_job(func=refetchAssets, trigger="interval", minutes=30)

    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    init_scheduler()
    app.run(debug=True)