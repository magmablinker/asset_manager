import os
import glob
import json
import base64
from flask import Blueprint, jsonify
from flask_cors import cross_origin
from dto.asset_response import AssetResponse
from dto.asset_profits_response import AssetProfitsResponse
from dto.asset_graph_response import AssetGraphResponse
from asset_manager.binance_asset import BinanceAsset

asset_controller = Blueprint("asset_controller", __name__)

@asset_controller.route("/asset/<asset_name>", methods=["GET"])
@cross_origin()
def get_asset_data(asset_name: str):
    asset_response = AssetResponse()
    asset_response.assets.append(asset_name)

    asset_path = f"data/assets/{asset_name}.json"

    if not os.path.exists(asset_path) and not os.path.isfile(asset_path):
        asset_response.response_code = 404
        asset_response.infos.add_error(f"No data available for asset {asset_name}")

        response = jsonify(asset_response.serialize())
        response.status_code = asset_response.response_code

        return response

    with open(asset_path, "r") as f:
        data = json.load(f)

        if "data" not in data:
            asset_response.response_code = 500
            asset_response.infos.add_error(f"Data in invalid format for asset {asset_name}")

            response = jsonify(asset_response.serialize())
            response.status_code = asset_response.response_code

            return response

        data["data"].sort(key=lambda x: x["timestamp"], reverse=True)
        asset_response.asset_data = data["data"]

        response = jsonify(asset_response.serialize())
        response.status_code = asset_response.response_code

        return response

@asset_controller.route("/asset", methods=["GET"])
@cross_origin()
def list_assets():
    asset_response = AssetResponse()

    files = [ os.path.basename(file).rsplit(".", 1)[0] for file in glob.glob("data/assets/*.json") ]

    asset_response.assets += files

    response = jsonify(asset_response.serialize())
    response.status_code = asset_response.response_code

    return response

@asset_controller.route("/asset/<asset_name>/graph", methods=["GET"])
@cross_origin()
def get_asset_graph(asset_name: str):
    asset_graph_response = AssetGraphResponse()
    
    if not os.path.exists(f"img/{asset_name}"):
        asset_graph_response.response_code = 404
        asset_graph_response.infos.add_error(f"No data available for asset {asset_name}")

        response = jsonify(asset_graph_response.serialize())
        response.status_code = asset_graph_response.response_code

        return response

    files = glob.glob(f"img/{asset_name}/*.png")

    if len(files) < 1:
        asset_graph_response.response_code = 404
        asset_graph_response.infos.add_error(f"No data available for asset {asset_name}")

        response = jsonify(asset_graph_response.serialize())
        response.status_code = asset_graph_response.response_code

        return response

    latest_file = max(files, key=os.path.getctime)

    with open(latest_file, "rb") as f:
        asset_graph_response.base64_img = base64.b64encode(f.read())

    response = jsonify(asset_graph_response.serialize())
    response.status_code = asset_graph_response.response_code

    return response

@asset_controller.route("/asset/<asset_name>/profits", methods=["GET"])
@cross_origin()
def get_asset_profits(asset_name: str):
    asset_profits_response = AssetProfitsResponse()

    try:
        binance_asset = BinanceAsset(asset_name, 0, "USDT")
        asset_profits_response.asset_profits = binance_asset.get_profits()
    except ValueError as e:
        asset_profits_response.infos.add_error(str(e))
        asset_profits_response.response_code = 404
    
    response = jsonify(asset_profits_response.serialize())
    response.status_code = asset_profits_response.response_code

    return response