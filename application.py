from flask import Flask
from controller.asset_controller import asset_controller
from controller.asset_manager_controller import asset_manager_controller

app = Flask(__name__)
app.register_blueprint(asset_controller)
app.register_blueprint(asset_manager_controller)

if __name__ == '__main__':
    app.run(debug=True)