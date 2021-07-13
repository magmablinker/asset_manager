from asset_manager.asset_manager import AssetManager
from flask import Flask

def main():
    asset_manager = AssetManager("config/config.json", "USDT")
    asset_manager.run()

    if asset_manager.debug:
        asset_manager.calculate_profits_from_inital_per_asset()

    asset_manager.binance_total_balance.to_graph()

    for asset in asset_manager.binance_assets:
        asset.to_graph()

if __name__ == '__main__':
    main()
