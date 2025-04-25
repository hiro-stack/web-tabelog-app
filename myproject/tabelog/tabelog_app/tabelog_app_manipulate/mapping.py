import pandas as pd
import folium
import math


class Mapping:
    def __init__(self, current_location):
        self.current_location = current_location
        self.input_csv_path = "data/result_data/result_data.csv"
        self.output_html_path = "data/result_data/mapping.html"

        # mappingするときの色の設定
        self.colors = ["red", "orange", "lightblue", "blue"]

        # 区切りポイント（1-3, 4-6, 7-10）
        self.segments = [10, 20, 30]

        self.mapping_df = pd.DataFrame()
        # 地図の初期化（現在地を中心）
        self.mymap = folium.Map(
            location=[
                self.current_location["latitude"],
                self.current_location["longitude"],
            ],
            zoom_start=12,
        )

    def main(self):
        self.app()

    def app(self):
        self.data_input()
        self.mapping_current_location()
        self.mapping_location()
        self.data_output()

    def data_input(self):
        self.mapping_df = pd.read_csv(self.input_csv_path)

    def mapping_current_location(self):
        folium.Marker(
            location=[
                self.current_location["latitude"],
                self.current_location["longitude"],
            ],
            popup=self.current_location["name"],
            icon=folium.Icon(color="black"),
        ).add_to(self.mymap)

    def mapping_location(self):
        for idx, row in self.mapping_df.head(30).iterrows():
            lat = row["緯度"]
            lon = row["経度"]
            name = row["店名"]
            score = row["点数"]

            score = math.floor(score * 100) / 100

            color = self.mapping_color(idx)
            print(color)
            self.add_mapping(lat, lon, name, score, color)
            print(idx, lat, lon, name, score, color)

    # 色の割り当て
    def mapping_color(self, idx):
        for i, segment in enumerate(self.segments):
            if idx <= segment:
                return self.colors[i]  # 対応する色を返す
        return self.colors[-1]  # それ以外の場合は最後の色

    # 地図の追加
    def add_mapping(self, lat, lon, name, score, color):
        folium.Marker(
            location=[lat, lon],
            popup=f"{name} ({score})",
            icon=folium.Icon(color=color),
        ).add_to(self.mymap)

    def data_output(self):
        self.mymap.save(self.output_html_path)
        print(f"地図が保存されました: {self.output_html_path}")


if __name__ == "__main__":
    current_location = {"name": "現在地", "latitude": 35.64338, "longitude": 139.66952}
    mapping = Mapping(current_location)
    mapping.main()
