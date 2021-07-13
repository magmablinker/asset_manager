from flask import Blueprint, jsonify
from asset_manager.asset_manager import AssetManager
from dto.assets_fetch_response import AssetsFetchResponse
from asset_manager.util.util import Util

asset_manager_controller = Blueprint("asset_manager_controller", __name__)

@asset_manager_controller.route("/asset_manager/fetch", methods=["PUT"])
def fetch_asset_data():
    assets_fetch_response = AssetsFetchResponse()
    asset_manager = AssetManager("config/config.json", "USDT")
    asset_manager.run()

    for asset in asset_manager.binance_assets:
        assets_fetch_response.add_asset(asset.asset, Util.round(asset.symbol_balance), asset.pair_asset)

    response = jsonify(assets_fetch_response.serialize())
    response.status_code = assets_fetch_response.response_code

    return response