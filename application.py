import matplotlib
matplotlib.use('Agg')

from flask import Flask
from flask_cors import CORS
from controller.asset_controller import asset_controller
from controller.asset_manager_controller import asset_manager_controller
from controller.total_balance_controller import total_balance_controller

app = Flask(__name__)
app.register_blueprint(asset_controller)
app.register_blueprint(asset_manager_controller)
app.register_blueprint(total_balance_controller)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/status")
def get_api_status():
    return {"status": "API Up and Running"}, 200

@app.before_first_request
def initialize():
    pass # TODO: Add scheduler

if __name__ == '__main__':
    app.run(debug=True)