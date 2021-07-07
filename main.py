from asset_manager.asset_manager import AssetManager

def main():
    asset_manager = AssetManager("config/config.json", True)
    asset_manager.calculate_profits_from_inital()
    #asset_manager.run()

if __name__ == '__main__':
    main()
