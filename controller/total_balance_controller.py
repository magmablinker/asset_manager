import os
import glob
import base64
from flask import Blueprint, jsonify
from flask_cors import cross_origin
from dto.total_balance_response import TotalBalanceResponse
from asset_manager.binance_total_balance import BinanceTotalBalance
from dto.asset_graph_response import AssetGraphResponse
from datetime import datetime
from dto.asset_profits_response import AssetProfitsResponse

total_balance_controller = Blueprint("total_balance_controller", __name__)

@total_balance_controller.route("/balance", methods=["GET"])
@cross_origin()
def get_total_balance():
    total_balance_response = TotalBalanceResponse()

    binance_total_balance = BinanceTotalBalance()

    try:
        total_balances = binance_total_balance.get_total_balance()
        total_balance_response.total_balance = total_balances["balance"]
        total_balance_response.timestamp = datetime.strptime(total_balances["timestamp"], "%d-%m-%Y %H:%M:%S")
    except ValueError as e:
        total_balance_response.infos.add_error(str(e))
        total_balance_response.response_code = 404

    response = jsonify(total_balance_response.serialize())
    response.status_code = total_balance_response.response_code

    return response

@total_balance_controller.route("/balance/graph", methods=["GET"])
@cross_origin()
def get_balance_graph():
    asset_graph_response = AssetGraphResponse()
    
    if not os.path.exists(f"img/total_balance.png"):
        asset_graph_response.response_code = 404
        asset_graph_response.infos.add_error(f"No data available for asset total balance")

        response = jsonify(asset_graph_response.serialize())
        response.status_code = asset_graph_response.response_code

        return response

    files = glob.glob(f"img/total_balance.png")

    if len(files) < 1:
        asset_graph_response.response_code = 404
        asset_graph_response.infos.add_error(f"No data available for asset total balance")

        response = jsonify(asset_graph_response.serialize())
        response.status_code = asset_graph_response.response_code

        return response

    latest_file = max(files, key=os.path.getctime)

    with open(latest_file, "rb") as f:
        asset_graph_response.base64_img = base64.b64encode(f.read())

    response = jsonify(asset_graph_response.serialize())
    response.status_code = asset_graph_response.response_code

    return response

@total_balance_controller.route("/balance/profits", methods=["GET"])
@cross_origin()
def get_balance_profits():
    asset_profits_response = AssetProfitsResponse()

    try:
        binance_asset = BinanceTotalBalance()
        asset_profits_response.asset_profits = binance_asset.get_profits()
    except ValueError as e:
        asset_profits_response.infos.add_error(str(e))
        asset_profits_response.response_code = 404
    
    response = jsonify(asset_profits_response.serialize())
    response.status_code = asset_profits_response.response_code

    return response