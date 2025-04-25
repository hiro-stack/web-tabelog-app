import os
import pandas as pd
import requests
from geopy.distance import geodesic
import urllib


class Geo:
    def __init__(self, current_location, dataframe):
        self.current_location = current_location
        self.input_output_folder = "data/maked_data"
        self.input_output_file = "combined_data.csv"
        self.shop_name_locations = []
        self.dataframe = dataframe

    def main(self):
        self.app()

    def app(self):
        # self.input_data()
        self.data_manipulate()
        # self.output_data()

    def input_data(self):
        input_file_path = os.path.join(self.input_output_folder, self.input_output_file)
        self.dataframe = pd.read_csv(input_file_path)

    def data_manipulate(self):
        self.dataframe["緯度"] = None
        self.dataframe["経度"] = None
        self.dataframe["現在地からの距離(km)"] = None

        for index, row in self.dataframe.iterrows():
            shop_location = self.get_geo_info(row["住所"])
            print(shop_location)
            distance = self.geopy_distance(self.current_location, shop_location)
            print(distance)

            self.dataframe_update(index, shop_location, distance)

            shop_name = row["店名"]
            shop_name_location = self.shop_name_distance_data_maked(
                shop_name, shop_location
            )
            self.shop_name_locations.append(shop_name_location)

        print(self.shop_name_locations)

    def dataframe_update(self, index, shop_location, distance):
        self.dataframe.at[index, "緯度"] = shop_location.get("latitude")
        self.dataframe.at[index, "経度"] = shop_location.get("longitude")
        self.dataframe.at[index, "現在地からの距離(km)"] = distance

    def shop_name_distance_data_maked(self, shop_name, shop_location):
        shop_name_location = {
            "店名": shop_name,
            "緯度": shop_location.get("latitude"),
            "経度": shop_location.get("longitude"),
        }

        return shop_name_location

    # 住所から緯度経度を取得
    def get_geo_info(self, address):
        makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
        s_quote = urllib.parse.quote(address)
        response = requests.get(makeUrl + s_quote)

        try:
            response_data = response.json()
            if not response_data:  # 空のリストチェック
                print(f"住所 '{address}' に対する結果が見つかりませんでした。")
                return {"latitude": None, "longitude": None}

            coordinates = response_data[0]["geometry"]["coordinates"]
            shop_location = {"latitude": coordinates[1], "longitude": coordinates[0]}
            return shop_location

        except Exception as e:
            print(f"住所 '{address}' の処理中にエラーが発生しました: {e}")
            return {"latitude": None, "longitude": None}

    # 2点の位置から緯度経度から距離を計算する
    def geopy_distance(self, location1, location2):
        if not location1["latitude"] or not location2["latitude"]:
            print("距離を計算できないデータが含まれています。")
            return None

        point1 = (location1["latitude"], location1["longitude"])
        point2 = (location2["latitude"], location2["longitude"])
        distance = geodesic(point1, point2).km
        return round(distance, 3)

    def output_data(self):
        output_file_path = os.path.join(
            self.input_output_folder, self.input_output_file
        )
        self.dataframe.to_csv(output_file_path, index=False, encoding="utf-8-sig")
        print("CSVファイルを出力しました:", output_file_path)


if __name__ == "__main__":
    current_location = {
        "name": "現在地",
        "latitude": 35.834774,
        "longitude": 139.912964,
    }
    geo = Geo(current_location)
    geo.main()
