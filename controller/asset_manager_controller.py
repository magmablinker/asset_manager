from flask import Blueprint, jsonify
from flask_cors import cross_origin
from asset_manager.asset_manager import AssetManager
from dto.assets_fetch_response import AssetsFetchResponse

asset_manager_controller = Blueprint("asset_manager_controller", __name__)

@asset_manager_controller.route("/asset_manager/fetch", methods=["PUT"])
@cross_origin()
def fetch_asset_data():
    assets_fetch_response = AssetsFetchResponse()
    asset_manager = AssetManager("config/config.json", "USDT")
    asset_manager.run()

    [ assets_fetch_response.add_asset(asset) for asset in asset_manager.binance_assets ]

    response = jsonify(assets_fetch_response.serialize())
    response.status_code = assets_fetch_response.response_code

    return response