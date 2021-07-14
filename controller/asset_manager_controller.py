from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from asset_manager.asset_manager import AssetManager
from dto.assets_fetch_response import AssetsFetchResponse
from dto.base_response import BaseResponse
from asset_manager.binance_total_balance import BinanceTotalBalance
from dto.config_dto import ConfigDto
from asset_manager.binance_config import BinanceConfig


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

@asset_manager_controller.route("/asset_manager/graph/generate", methods=["PUT"])
@cross_origin()
def generate_graphs():
    base_response = BaseResponse()
    asset_manager = AssetManager("config/config.json", "USDT")

    for asset in asset_manager.binance_assets:
        asset.to_graph()

    total_balance = BinanceTotalBalance()
    total_balance.to_graph()

    base_response.infos.add_message("Successfully generated graphs")

    return jsonify(base_response.serialize())

@asset_manager_controller.route("/asset_manager/config", methods=["GET"])
@cross_origin()
def get_asset_manager_config():
    config_response = ConfigDto()
    
    try:
        binance_config = BinanceConfig("config/config.json")

        config_response.config = {
            "api_key": binance_config.api_key,
            "api_secret": binance_config.api_secret,
            "debug": binance_config.debug,
            "asset_blacklist": binance_config.asset_blacklist
        }
    except Exception as e:
        config_response.infos.add_error(str(e))
        config_response.response_code = 500

    response = jsonify(config_response.serialize())
    response.status_code = config_response.response_code

    return response

@asset_manager_controller.route("/asset_manager/config", methods=["PUT"])
@cross_origin()
def update_asset_manager_config():
    base_response = BaseResponse()
    data = request.get_json()
    binance_config = BinanceConfig("config/config.json")

    if "api_key" not in data:
        base_response.infos.add_error("API Key is a required key!")
        base_response.response_code = 400
        
    if "api_secret" not in data:
        base_response.infos.add_error("API Secret is a required key!")
        base_response.response_code = 400

    if "debug" not in data:
        base_response.infos.add_error("Debug is a required key!")
        base_response.response_code = 400

    if "asset_blacklist" not in data:
        base_response.infos.add_error("Asset_blacklist is a required key!")
        base_response.response_code = 400

    if not base_response.infos.has_error:
        binance_config.api_key = data["api_key"]
        binance_config.api_secret = data["api_secret"]
        binance_config.debug = data["debug"]
        binance_config.asset_blacklist = data["asset_blacklist"]

        try:
            binance_config.save_config()
            base_response.infos.add_message("Successfully saved the config")
        except Exception as e:
            base_response.infos.add_error(str(e))
            base_response.response_code = 500


    response = jsonify(base_response.serialize())
    response.status_code = base_response.response_code

    return response