from asset_manager.asset_manager import AssetManager

def main():
    asset_manager = AssetManager("config/config.json", True)
    asset_manager.run()
    asset_manager.calculate_profits_from_inital_per_asset()

if __name__ == '__main__':
    main()
