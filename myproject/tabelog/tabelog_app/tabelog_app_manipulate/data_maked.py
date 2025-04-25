import os
import pandas as pd
from glob import glob
import re
from .geo import Geo

class DataMaker:
    
    """
    Attributes:
        current_location (dict): 現在地の緯度と経度情報を含む辞書。
        voice_force (dict): 項目ごとの「声の大きさ」の値。
        csv_files (list[str]): 入力フォルダ内のCSVファイルパスのリスト。
        input_folder_path (str): 入力データのフォルダパス。
        output_folder_path (str): 出力データのフォルダパス。
        output_csv_name (str): 出力するCSVファイル名。
        required_columns (list[str]): 必須のカラム名リスト。
        combined_df (pd.DataFrame): 統合されたデータフレーム。
        walk_speed_kmh (float): 徒歩の速度 (km/h)。
    """


    def __init__(self, current_location, votes_result, alpha):
        self.votes_result = votes_result
        self.alpha = alpha
        self.voice_results = {}
        self.csv_files = []
        self.input_folder_path = 'data/source_data'
        self.output_folder_path = 'data/maked_data'
        self.output_csv_name = 'combined_data.csv'
        self.required_columns = ["星5段階評価", "店名", "住所", "Dinner", "Lunch", "項目"]
        self.combined_df = pd.DataFrame()
        self.current_location = current_location
        
        #歩くスピードの定義(km/h)
        self.walk_speed_kmh = 4.0


    def main(self):
        self.app()

    def app(self):
        self.data_input()
        self.data_maked()
        self.output_data()

    #パスからcsvファイルのパスを取得する
    def data_input(self):
        current_path = os.getcwd()
        source_dir = os.path.join(current_path, self.input_folder_path)
        self.csv_files = glob(os.path.join(source_dir, "*", "*.csv"))
        print(self.csv_files)


    #全てのCVSファイルを読み込む
    def data_maked(self):
        data_frames = []
        for file_path in self.csv_files:
            df = pd.read_csv(file_path)
            df = self.process_data(df, file_path)
            df = df[self.required_columns]
            data_frames.append(df)

        # すべてのデータフレームを連結
        self.combined_df = pd.concat(data_frames, ignore_index=True)

        #地理に関するデータを付け足す関数
        self.geo_manipulate()

        #声の大きさに関するデータのつけ足しに関する関数
        self.voice_force_manipulate()

        #重複しているデータを省く
        self.combined_df = self.combined_df.drop_duplicates()

        #数値データでないときに数値データに直す
        self.combined_df = self.ensure_numeric_columns(self.combined_df)
    
    def voice_force_manipulate(self):
        self.calculate_score(self.votes_result, self.alpha)
        self.combined_df['声の大きさ'] = self.combined_df["項目"].map(self.voice_results)

    #voter_resultとalphaから食べ物ごとのスコアを計算
    def calculate_score(self, votes, alpha):
        for option, scores in votes.items():
            total_weight = sum(scores)  # 重要度スコアの合計
            vote_count = len(scores)   # 投票人数
            # スコア計算: 重要度スコアと投票数を重み付け
            score = (1 - alpha) * total_weight + alpha * vote_count
            self.voice_results[option] = score

    
    def geo_manipulate(self):
        self.geo = Geo(self.current_location, self.combined_df)
        self.geo.main()
    
        self.combined_df["現在地点からの徒歩(分)"] = self.combined_df["現在地からの距離(km)"].apply(
        lambda x: (x / self.walk_speed_kmh) * 60 if x is not None else None
        )
        self.combined_df.dropna(subset=["現在地点からの徒歩(分)"], inplace=True)


     #データフレームに非数値データが含まれた場合に数値データに変換する
    def ensure_numeric_columns(self, df):
        # 数値に変換したい列
        numeric_columns = ['星5段階評価', 'Dinner', 'Lunch', '緯度', '経度', '現在地からの距離(km)', '現在地点からの徒歩(分)', '声の大きさ']
        
        for col in numeric_columns:
            # 数値に変換し、エラーが出る場合はNaNに変換
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # NaNを含む行を削除
        df.dropna(subset=numeric_columns, inplace=True)
        return df


    #読み込んだcsvファイルの加工内容
    def process_data(self, df, filepath):
        df = self.remove_rows_no_star_rating(df)
        df = self.remove_rows_no_address(df)
        df = self.process_dinner(df)
        df = self.process_lunch(df)
        df = self.add_item_column(df, filepath)
        return df

    # 「星5段階評価」がない行を除外する
    def remove_rows_no_star_rating(self, df):
        df = df.dropna(subset=['星5段階評価'])
        df = df[df['星5段階評価'] != "None-info"]
        return df
    
    # 「住所」がない行を除外する
    def remove_rows_no_address(self, df):
        df = df.dropna(subset=['住所'])
        return df

    # 「dinner」の項目から平均値を算出する
    def process_dinner(self, df):
        df['Dinner'] = df['Dinner'].apply(self.extract_average_price)
        return df

    # 「lunch」の項目から平均値を算出する
    def process_lunch(self, df):
        df['Lunch'] = df['Lunch'].apply(self.extract_average_price)
        return df

    
    # ファイル名から「項目」列を作成する
    def add_item_column(self, df, filepath):
        item_name = os.path.splitext(os.path.basename(filepath))[0]
        df['項目'] = item_name
        return df

    # 価格範囲から平均を取り出すヘルパーメソッド
    def extract_average_price(self, price_str):
        if pd.isna(price_str):
            return 0  # 値がなければ0を設定

        # 正規表現で整数を抽出
        # カンマ付きの数字を含めて抽出し、"~" や範囲指定（"～"）も考慮
        prices = list(map(lambda x: int(x.replace(',', '')), re.findall(r'\d{1,3}(?:,\d{3})*', price_str)))
        if prices:
            return sum(prices) // len(prices)  # 平均値を返す
        return 0  # 数字が見つからなければ0を返す
    



    #結果を保存する
    def output_data(self):
       self.output_data_folder_make()
       self.output_data_file()

       
    # output用のフォルダーの作成
    def output_data_folder_make(self):
        current_path = os.getcwd()
        output_dir = os.path.join(current_path, self.output_folder_path)
        os.makedirs(output_dir, exist_ok=True)


    # 連結したデータをCSVファイルとして保存
    def output_data_file(self):
       current_path = os.getcwd()
       output_path = os.path.join(current_path, self.output_folder_path, self.output_csv_name)
       self.combined_df.to_csv(output_path, index=False, encoding="utf-8-sig")

       print("連結したデータを保存しました:", output_path)


if __name__ == "__main__":

    current_location = {
        'name': "現在地",
        'latitude': 35.834774,
        'longitude': 139.912964
    }

    voice_force = {'ラーメン': 3, '寿司': 2, '焼肉': 1}

    app = DataMaker(current_location, voice_force)
    app.main()